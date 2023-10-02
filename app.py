import os
import uuid
import smtplib
import subprocess
import io
import openai
from flask import Flask, request, jsonify, send_from_directory, current_app
from werkzeug.utils import secure_filename
from models import db, SavedVideo
from helpers import *
from datetime import datetime
from moviepy.editor import VideoFileClip, concatenate_videoclips, clips_array
from email.mime.text import MIMEText

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['UPLOAD_FOLDER'] = 'videos'

openai.api_key = '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'


# Initialize the database
db.init_app(app)

# Create the database tables
with app.app_context():
    db.create_all()

# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Define allowed file extensions
ALLOWED_EXTENSIONS = {"mp4", "mov", "wmv", "avi", "mkv", "flv", "webm"}

# Function to check if a file has an allowed extension


def allowed_video_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/api/submit_record', methods=['POST'])
def submit_record():
    try:
        # Check if the POST request has a file part
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        file = request.files['file']

        # If the user does not select a file, the browser may send an empty file without a filename
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        # Check if the file has an allowed extension
        if not allowed_video_file(file.filename):
            return jsonify({'error': 'File extension not allowed'}), 400

        # Generate a UUID for the video URL
        video_uuid = str(uuid.uuid4())

        # Construct a new file name using the UUID and the allowed extension
        filename = f'{video_uuid}.{file.filename.rsplit(".", 1)[1].lower()}'

        # Save the uploaded video to a temporary location
        temp_video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        # temp_video_path = os.path.abspath(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        file.save(temp_video_path)

        # Create a VideoFileClip object for the uploaded video
        video = VideoFileClip(temp_video_path)
        # Define the output path for the compressed video
        compressed_video_path = os.path.join(
            app.config['UPLOAD_FOLDER'], 'compressed_' + filename)
        compressed_video = video.write_videofile(
            compressed_video_path, bitrate="500k")

        # Close the VideoFileClip objects
        # video.close()
        # compressed_video.close()

        # Transcribe the video's audio using Openai Whisper ASR
        # audio_file= open(compressed_video_path, "rb")
        # response = openai.Audio.transcribe(
        #     "whisper-1",
        #     audio_file,
        #     language="en-US",
        # )

        # # Extract the transcribed text from the API response
        # audio_transcript = response['text']

        # Transcribe the video's audio content using sr
        audio_transcript = transcribe_audio(compressed_video_path)

        # Use the save_video_to_database function
        saved_video = SavedVideo()
        vide = open(compressed_video_path, 'rb').read()
        url = f'https://HelpMeOut.com/videos/{video_uuid}'

        if saved_video.save_video_to_database(filename, vide, url, audio_transcript):
            # Delete the temporary file after saving to the database
            os.remove(compressed_video_path)
            os.remove(temp_video_path)
            return jsonify({
                'message': 'Recorded content received successfully',
                'video_url': f'https://HelpMeOut.com/videos/{video_uuid}'
            }), 200
        else:
            return jsonify({'error': 'Failed to save video to the database'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/get_all_videos', methods=['GET'])
def get_all_videos():
    try:
        # Get all videos from the database.
        videos = SavedVideo.query.all()

        video_data = []

        for video in videos:
            # Calculate the video size in megabytes
            video_size_mb = len(video.video_file) / \
                (1024 * 1024)  # Bytes to Megabytes

            video_data.append({
                'id': video.id,
                'name': video.name,
                'video_url': video.video_url,
                'transcript': video.transcript,
                'date_created': video.date_created.isoformat(),
                'video_size_mb': video_size_mb,
            })

        # Return the list of video data as a JSON response
        return jsonify({'videos': video_data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/get_video/<name>', methods=['GET'])
def get_video_details(name):
    try:
        # Query the database for the video with the specified URL
        video = SavedVideo.query.filter_by(name=name).first()

        if not video:
            return jsonify({'error': 'Video not found'}), 404

        # Calculate the video size in megabytes
        video_size_mb = len(video.video_file) / \
            (1024 * 1024)  # Bytes to Megabytes

        # Prepare the video data response
        video_data = {
            'id': video.id,
            'name': video.name,
            'video_url': video.video_url,
            'transcript': video.transcript,
            'date_created': video.date_created.isoformat(),
            'video_size_mb': video_size_mb  # Include video size in MB
        }

        # Return the video data as a JSON response
        return jsonify({'video': video_data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/get_video/<name>', methods=['PUT'])
def update_video_details(name):
    try:
        # Query the database for the video with the specified name
        video = SavedVideo.query.filter_by(name=name).first()

        if not video:
            return jsonify({'error': 'Video not found'}), 404

        # Update video details based on the PUT request data
        data = request.get_json()
        if 'transcript' in data:
            video.transcript = data['transcript']

        # Commit the changes to the database
        db.session.commit()

        # Return a success message
        return jsonify({'message': 'Video details updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/get_video/<name>', methods=['DELETE'])
def delete_video(name):
    try:
        # Query the database for the video with the specified name
        video = SavedVideo.query.filter_by(name=name).first()

        if not video:
            return jsonify({'error': 'Video not found'}), 404

        # Delete the video from the database
        db.session.delete(video)
        db.session.commit()

        # Return a success message
        return jsonify({'message': 'Video deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/get_video/<video_url>', methods=['GET'])
def get_video_details_by_url(video_url):
    try:
        # Query the database for the video with the specified URL
        video = SavedVideo.query.filter_by(video_url=video_url).first()

        if not video:
            return jsonify({'error': 'Video not found'}), 404

        # Calculate the video size in megabytes
        video_size_mb = len(video.video_file) / \
            (1024 * 1024)  # Bytes to Megabytes

        # Prepare the video data response
        video_data = {
            'id': video.id,
            'name': video.name,
            'video_url': video.video_url,
            'transcript': video.transcript,
            'date_created': video.date_created.isoformat(),
            'video_size_mb': video_size_mb  # Include video size in MB
        }

        # Return the video data as a JSON response
        return jsonify({'video': video_data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/update_video/<video_url>', methods=['PUT'])
def update_video_details_by_url(video_url):
    try:
        # Query the database for the video with the specified URL
        video = SavedVideo.query.filter_by(video_url=video_url).first()

        if not video:
            return jsonify({'error': 'Video not found'}), 404

        # Update video details based on the PUT request data
        data = request.get_json()
        if 'transcript' in data:
            video.transcript = data['transcript']

        # Commit the changes to the database
        db.session.commit()

        # Return a success message
        return jsonify({'message': 'Video details updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/delete_video/<video_url>', methods=['DELETE'])
def delete_video_by_url(video_url):
    try:
        # Query the database for the video with the specified URL
        video = SavedVideo.query.filter_by(video_url=video_url).first()

        if not video:
            return jsonify({'error': 'Video not found'}), 404

        # Delete the video from the database
        db.session.delete(video)
        db.session.commit()

        # Return a success message
        return jsonify({'message': 'Video deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route("/api/cut_video/<video_name>", methods=["PUT"])
def cut_video(video_name):
    try:
        # Get the start_time and end_time from the request body
        start_time = request.json.get("start_time")
        end_time = request.json.get("end_time")

        # Query the database for the video with the specified video_name
        video = SavedVideo.query.filter_by(name=video_name).first()

        if not video:
            return jsonify({'error': 'Video not found'}), 404

        # Create a temporary file to store the video content
        temp_video_path = os.path.join(
            app.config['UPLOAD_FOLDER'], 'temp_' + video_name)

        with open(temp_video_path, 'wb') as temp_video_file:
            temp_video_file.write(video.video_file)

        # Create a VideoFileClip object for the video from the temporary file
        video_clip = VideoFileClip(temp_video_path)

        # Cut out the part of the video from the start_time to the end_time
        cut_video_clip = video_clip.subclip(start_time, end_time)

        # Write the cut video to a temporary file
        chunked_path = os.path.join(
            app.config['UPLOAD_FOLDER'], 'dissect_' + video_name)
        cut_video_clip.write_videofile(chunked_path, codec="libx264")

        # Transcribe the video's audio using Whisper ASR
        audio_transcript = transcribe_audio(chunked_path)

        # Update the existing video's transcript and video_file
        video.transcript = audio_transcript
        video.video_file = open(chunked_path, "rb").read()

        # Commit the changes to the database
        db.session.commit()

        # Delete the temporary files after saving to the database
        os.remove(temp_video_path)
        os.remove(chunked_path)

        # Return the URL of the updated video
        return jsonify({
            "message": "Video cut and updated successfully",
            "video_url": f"https://HelpMeOut.com/videos/{video_name}",
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/concatenate_videos', methods=['POST'])
def concatenate_videos():
    try:
        # Check if the POST request has 'video_files' parts
        if 'video_files' not in request.files:
            return jsonify({'error': 'No video files provided'}), 400

        video_files = request.files.getlist('video_files')

        if len(video_files) < 2:
            return jsonify({'error': 'Provide at least two video files'}), 400

        # Generate UUID for the concatenated video
        concatenated_video_uuid = str(uuid.uuid4())
        concatenated_filename = f'concatenated_{concatenated_video_uuid}.mp4'
        concatenated_video_path = os.path.join(
            app.config['UPLOAD_FOLDER'], concatenated_filename)

        # Create a list of VideoFileClip objects for the uploaded videos
        video_clips = []
        for video_file in video_files:
            if not allowed_video_file(video_file.filename):
                return jsonify({'error': 'File extension not allowed'}), 400

            temp_video_path = os.path.join(
                app.config['UPLOAD_FOLDER'], f'temp_{uuid.uuid4()}.mp4')
            video_file.save(temp_video_path)

            video_clip = VideoFileClip(temp_video_path)
            video_clips.append(video_clip)

            os.remove(temp_video_path)  # Remove the temporary file

        # Concatenate the video clips
        concatenated_clip = concatenate_videoclips(
            video_clips, method="compose")

        # Write the concatenated video to a file
        concatenated_clip.write_videofile(
            concatenated_video_path, codec="libx264")

        # Transcribe the audio of the concatenated video
        audio_transcript = transcribe_audio(concatenated_video_path)

        # Use the save_video_to_database function
        saved_video = SavedVideo()
        video_bytes = open(concatenated_video_path, 'rb').read()
        video_url = f'https://HelpMeOut.com/videos/{concatenated_video_uuid}'

        if saved_video.save_video_to_database(concatenated_filename, video_bytes, video_url, audio_transcript):
            return jsonify({
                'message': 'Concatenated video received and saved successfully',
                'video_url': video_url
            }), 200
        else:
            return jsonify({'error': 'Failed to save video to the database'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/submit_to_email/<video_name>', methods=['POST'])
def submit_to_email(video_name):
    try:
        # Query the database for the SavedVideo with the specified video_id
        video = SavedVideo.query.get(video_name)

        # Get data from the POST request
        data = request.get_json()

        name = data.get('name')
        email = data.get('email')

        # Query the database for the SavedVideo with the specified video_name
        if not video:
            return jsonify({'error': 'Video not found'}), 404

        # Extract name and video_url from the SavedVideo object
        video_url = video.video_url

        # Set up the email content and send it to the email
        subject = 'New Video Submission'
        message = f'Name: {name}\nVideo URL: {video_url}'

        # Set up the email configuration (use your SMTP server and credentials)
        smtp_server = 'your_smtp_server.com'
        smtp_port = 587
        smtp_username = 'your_email@example.com'
        smtp_password = 'your_email_password'

        # Create an SMTP connection
        server = smtplib.SMTP(smtp_server, smtp_port)

        # Start the TLS encryption (secure connection)
        server.starttls()

        # Login to the SMTP server
        server.login(smtp_username, smtp_password)

        # Create the email message
        msg = MIMEText(message)
        msg['From'] = smtp_username
        msg['To'] = email
        msg['Subject'] = subject

        # Send the email
        server.sendmail(smtp_username, email, msg.as_string())

        # Close the SMTP server connection
        server.quit()

        return jsonify({'message': 'Email sent successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)

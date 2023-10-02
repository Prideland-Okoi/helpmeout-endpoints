import speech_recognition as sr


# Define allowed file extensions
ALLOWED_EXTENSIONS = {"mp4", "mov", "wmv", "avi", "mkv", "flv", "webm"}

# Function to check if a file has an allowed extension
def allowed_video_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def transcribe_audio(audio_path):
    try:
        r = sr.Recognizer()

        with sr.AudioFile(audio_path) as source:
            audio_data = r.record(source)  # Record the entire audio file

        # Use the Google Web Speech API for transcription
        transcription = r.recognize_google(audio_data)

        return transcription
    except Exception as e:
        return str(e)


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

def extract_name_from_url(video_url):
    # Split the UUID using "com/" as the separator and take the second part
    parts = url.split("com/")
    
    if len(parts) == 2:
        return parts[1]
    elif len(parts) >= 3:
        return parts[-1]
    else:
        return None


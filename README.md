# Video Processing and Management API

The Video Processing and Management API is a RESTful web service built using Flask, designed for processing and managing video files. This API allows users to upload, transcode, edit, and manage videos efficiently. It includes features such as video compression, audio transcription, cutting, concatenation, and more.

## Features

- **Video Upload:** Users can upload video files in various formats (e.g., mp4, mov, avi) to the API.

- **Video Compression:** Uploaded videos are automatically compressed to reduce file size while maintaining quality.

- **Audio Transcription:** The API can transcribe the audio content of videos using the OpenAI Whisper ASR system.

- **Video Editing:**

  - **Cutting:** Users can specify start and end times to cut out a portion of a video.
  - **Concatenation:** Multiple video clips can be concatenated into a single video.

- **Video Management:** Users can retrieve, update, and delete video records stored in the database.

- **Email Submission:** Users can submit videos to specific email addresses.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.6 or higher installed.
- Dependencies installed (Flask, SQLAlchemy, MoviePy, OpenAI, etc.).

You can install the required dependencies using `pip`:

```bash
pip install Flask flask_sqlalchemy moviepy openai
```

## Configuration

Before running the API, configure the following settings in the `config.py` file:

- `SQLALCHEMY_DATABASE_URI`: URI of the SQLite database.
- `SECRET_KEY`: A secret key for securing the application.
- `UPLOAD_FOLDER`: Folder where uploaded videos are stored.
- `openai.api_key`: Your OpenAI API key for audio transcription (optional).

Ensure you replace the placeholder values with your actual configuration.

## Usage

To run the API, execute the following command:

```bash
python app.py
```

The API will start on `http://localhost:5000`.

## API Endpoints

The API provides the following endpoints:

- **Submit a Video Record:** `/api/submit_record` (POST)
- **Get All Videos:** `/api/get_all_videos` (GET)
- **Get Video Details by Name:** `/api/get_video/<name>` (GET)
- **Update Video Details by Name:** `/api/update_video/<name>` (PUT)
- **Delete Video by Name:** `/api/delete_video/<name>` (DELETE)
- **Get Video Details by URL:** `/api/get_video/<video_url>` (GET)
- **Update Video Details by URL:** `/api/update_video/<video_url>` (PUT)
- **Delete Video by URL:** `/api/delete_video/<video_url>` (DELETE)
- **Cut Video:** `/api/cut_video/<video_name>` (PUT)
- **Concatenate Videos:** `/api/concatenate_videos` (POST)
- **Submit Video to Email:** `/api/submit_to_email/<video_name>` (POST)

Refer to the [API Documentation](https://github.com/Prideland-Okoi/helpmeout-endpoints/blob/main/DOCUMENTATION.md) for detailed information on each endpoint.

## Contribution

Contributions are welcome! If you'd like to contribute to the project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes and push them to your fork.
4. Create a pull request to the main repository.

## License

This project is licensed under the MIT License. See the [LICENSE](https://mit-license.org/) file for details.

## Contact

If you have any questions or need further assistance, feel free to contact us:

- Email: [your.email@example.com](mailto:prideland.okoi@gmail.com)
- GitHub: [Your GitHub Profile](https://github.com/Prideland-Okoi)

## Acknowledgments

- [Flask](https://flask.palletsprojects.com/): Web framework used for building the API.
- [MoviePy](https://zulko.github.io/moviepy/): Python library for video editing.
- [OpenAI Whisper ASR](https://beta.openai.com/whisper): Automatic Speech Recognition system for audio transcription.

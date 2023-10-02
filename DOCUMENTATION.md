# Video Processing and Management API Documentation

This documentation provides an overview of the Video Processing and Management API. This API allows you to submit, retrieve, update, and delete videos, as well as perform various video processing tasks such as cutting and concatenating videos. The API is built using Flask and uses SQLAlchemy to interact with a SQLite database.

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Endpoints](#endpoints)
  - [Submit a Video Record](#submit-a-video-record)
  - [Get All Videos](#get-all-videos)
  - [Get Video Details by Name](#get-video-details-by-name)
  - [Update Video Details by Name](#update-video-details-by-name)
  - [Delete Video by Name](#delete-video-by-name)
  - [Get Video Details by URL](#get-video-details-by-url)
  - [Update Video Details by URL](#update-video-details-by-url)
  - [Delete Video by URL](#delete-video-by-url)
  - [Cut Video](#cut-video)
  - [Concatenate Videos](#concatenate-videos)
  - [Submit Video to Email](#submit-video-to-email)

## Installation

Before using the API, make sure you have the required dependencies installed. You can install them using pip:

```bash
pip install Flask flask_sqlalchemy moviepy openai
```

## Configuration

Before running the API, you need to configure the following settings in the `app.config` object within the script:

- `SQLALCHEMY_DATABASE_URI`: The URI of the SQLite database.
- `SECRET_KEY`: A secret key for securing the application.
- `UPLOAD_FOLDER`: The folder where uploaded videos are stored.
- `openai.api_key`: Your OpenAI API key for audio transcription (optional).

Ensure that you replace the placeholder values with your actual configuration.

## Endpoints

### Submit a Video Record

**Endpoint:** `/api/submit_record`
**Method:** `POST`
**Description:** Submit a video for processing, which includes video compression, audio transcription, and saving to the database.

#### Request Parameters

- `file` (multipart/form-data): The video file to be submitted.

#### Response

- 200 OK: Video successfully submitted, processed, and saved.
- 400 Bad Request: Invalid request format or missing file part.
- 500 Internal Server Error: Failed to save video to the database.

#### Example Request

```bash
curl -X POST -F "file=@video.mp4" https://helpmeout-endpoints.onrender.com/api/submit_record
```

#### Example Response

```json
{
  "message": "Recorded content received successfully",
  "video_url": "https://HelpMeOut.com/videos/{video_uuid}"
}
```

### Get All Videos

**Endpoint:** `/api/get_all_videos`
**Method:** `GET`
**Description:** Retrieve a list of all saved videos from the database.

#### Response

- 200 OK: List of videos successfully retrieved.
- 500 Internal Server Error: Failed to retrieve videos from the database.

#### Example Request

```bash
curl https://helpmeout-endpoints.onrender.com/api/get_all_videos
```

#### Example Response

```json
{
  "videos": [
    {
      "id": 1,
      "name": "video1.mp4",
      "video_url": "https://HelpMeOut.com/videos/{video_uuid}",
      "transcript": "Transcribed text for video 1",
      "date_created": "2023-10-02T12:34:56",
      "video_size_mb": 12.34
    },
    {
      "id": 2,
      "name": "video2.mp4",
      "video_url": "https://HelpMeOut.com/videos/{video_uuid}",
      "transcript": "Transcribed text for video 2",
      "date_created": "2023-10-02T13:45:00",
      "video_size_mb": 8.56
    }
  ]
}
```

### Get Video Details by Name

**Endpoint:** `/api/get_video/<name>`
**Method:** `GET`
**Description:** Retrieve details of a specific video by its name.

#### Response

- 200 OK: Video details successfully retrieved.
- 404 Not Found: Video with the specified name not found.
- 500 Internal Server Error: Failed to retrieve video details.

#### Example Request

```bash
curl https://helpmeout-endpoints.onrender.com/api/get_video/video1.mp4
```

#### Example Response

```json
{
  "video": {
    "id": 1,
    "name": "video1.mp4",
    "video_url": "https://HelpMeOut.com/videos/{video_uuid}",
    "transcript": "Transcribed text for video 1",
    "date_created": "2023-10-02T12:34:56",
    "video_size_mb": 12.34
  }
}
```

### Update Video Details by Name

**Endpoint:** `/api/update_video/<name>`
**Method:** `PUT`
**Description:** Update the transcript of a specific video by its name.

#### Request Body

- `transcript` (string): The new transcript for the video.

#### Response

- 200 OK: Video details successfully updated.
- 404 Not Found: Video with the specified name not found.
- 500 Internal Server Error: Failed to update video details.

#### Example Request

```bash
curl -X PUT -H "Content-Type: application/json" -d '{"transcript": "Updated transcript"}' https://helpmeout-endpoints.onrender.com/api/update_video/video1.mp4
```

#### Example Response

```json
{
  "message": "Video details updated successfully"
}
```

### Delete Video by Name

**Endpoint:** `/api/delete_video/<name>`
**Method:** `DELETE`
**Description:** Delete a specific video by its name.

#### Response

- 200 OK: Video successfully deleted.
- 404 Not Found: Video with the specified name not found.
- 500 Internal Server Error: Failed to delete video.

#### Example Request

```bash
curl -X DELETE https://helpmeout-endpoints.onrender.com/api/delete_video/video1.mp4
```

#### Example Response

```json
{
  "message": "Video deleted successfully"
}
```

### Get Video Details by URL

**Endpoint:** `/api/get_video/<video_url>`
**Method:** `GET`
**Description:** Retrieve details of a specific video by its URL.

#### Response

- 200 OK: Video details successfully retrieved.
- 404 Not Found: Video with the specified URL not found.
- 500 Internal Server Error: Failed to retrieve video details.

#### Example Request

```bash
curl https://helpmeout-endpoints.onrender.com/api/get_video/https://HelpMeOut.com/videos/{video_uuid}
```

#### Example Response

```json
{
  "video": {
    "id": 1,
    "name": "video1.mp4",
    "video_url": "https://HelpMeOut.com/videos/{video_uuid}",
    "transcript": "Transcribed text for video 1",
    "date_created": "2023-10-02T12:34:56",
    "video_size_mb": 12.34
  }
}
```

### Update Video Details by URL

**Endpoint:** `/api/update_video/<

video_url>`**Method:**`PUT`
**Description:** Update the transcript of a specific video by its URL.

#### Request Body

- `transcript` (string): The new transcript for the video.

#### Response

- 200 OK: Video details successfully updated.
- 404 Not Found: Video with the specified URL not found.
- 500 Internal Server Error: Failed to update video details.

#### Example Request

```bash
curl -X PUT -H "Content-Type: application/json" -d '{"transcript": "Updated transcript"}' https://helpmeout-endpoints.onrender.com/api/update_video/https://HelpMeOut.com/videos/{video_uuid}
```

#### Example Response

```json
{
  "message": "Video details updated successfully"
}
```

### Delete Video by URL

**Endpoint:** `/api/delete_video/<video_url>`
**Method:** `DELETE`
**Description:** Delete a specific video by its URL.

#### Response

- 200 OK: Video successfully deleted.
- 404 Not Found: Video with the specified URL not found.
- 500 Internal Server Error: Failed to delete video.

#### Example Request

```bash
curl -X DELETE https://helpmeout-endpoints.onrender.com/api/delete_video/https://HelpMeOut.com/videos/{video_uuid}
```

#### Example Response

```json
{
  "message": "Video deleted successfully"
}
```

### Cut Video

**Endpoint:** `/api/cut_video/<video_name>`
**Method:** `PUT`
**Description:** Cut a specific video by its name, specifying start and end times.

#### Request Body

- `start_time` (float): The start time in seconds.
- `end_time` (float): The end time in seconds.

#### Response

- 200 OK: Video successfully cut and updated.
- 404 Not Found: Video with the specified name not found.
- 500 Internal Server Error: Failed to cut and update the video.

#### Example Request

```bash
curl -X PUT -H "Content-Type: application/json" -d '{"start_time": 10, "end_time": 30}' https://helpmeout-endpoints.onrender.com/api/cut_video/video1.mp4
```

#### Example Response

```json
{
  "message": "Video cut and updated successfully",
  "video_url": "https://HelpMeOut.com/videos/{video_uuid}"
}
```

### Concatenate Videos

**Endpoint:** `/api/concatenate_videos`
**Method:** `POST`
**Description:** Concatenate multiple videos into a single video.

#### Request Parameters

- `video_files` (multipart/form-data): The list of video files to concatenate.

#### Response

- 200 OK: Videos successfully concatenated and saved.
- 400 Bad Request: Invalid request format or fewer than two video files provided.
- 500 Internal Server Error: Failed to save the concatenated video to the database.

#### Example Request

```bash
curl -X POST -F "video_files=@video1.mp4" -F "video_files=@video2.mp4" https://helpmeout-endpoints.onrender.com/api/concatenate_videos
```

#### Example Response

```json
{
  "message": "Concatenated video received and saved successfully",
  "video_url": "https://HelpMeOut.com/videos/{video_uuid}"
}
```

### Submit Video to Email

**Endpoint:** `/api/submit_to_email/<video_name>`
**Method:** `POST`
**Description:** Submit a video to an email address.

#### Request Body

- `name` (string): The name of the recipient.
- `email` (string): The email address of the recipient.

#### Response

- 200 OK: Email sent successfully.
- 404 Not Found: Video with the specified name not found.
- 500 Internal Server Error: Failed to send the email.

#### Example Request

```bash
curl -X POST -H "Content-Type: application/json" -d '{"name": "John Doe", "email": "john@example.com"}' https://helpmeout-endpoints.onrender.com/api/submit_to_email/video1.mp4
```

#### Example Response

```json
{
  "message": "Email sent successfully"
}
```

## Conclusion

This API provides various video processing and management capabilities, including uploading, retrieving, updating, and deleting videos, as well as performing video editing tasks such as cutting and concatenating. It also supports sending video submissions via email.

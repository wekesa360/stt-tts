# Speech-to-Text and Text-to-Speech API

This project implements a FastAPI-based web service that provides Speech-to-Text (STT) and Text-to-Speech (TTS) functionality. It includes endpoints for converting audio to text, text to audio, and a debug endpoint for generating test audio.

## Features

- Speech-to-Text (STT) conversion
- Text-to-Speech (TTS) conversion
- API key authentication
- Debug endpoint for audio generation
- Logging for better traceability and debugging

## Prerequisites

- Python 3.9+
- Docker (optional, for containerized deployment)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/stt-tts-api.git
   cd stt-tts-api
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Running the Server

To start the server, run:

```
python main.py
```

The server will start on `http://0.0.0.0:8000`.

### API Endpoints

1. **Speech-to-Text (STT)**
   - URL: `/stt`
   - Method: POST
   - Headers:
     - `X-App-ID`: Your App ID
     - `X-App-Key`: Your App Key
   - Body: Raw audio file

2. **Text-to-Speech (TTS)**
   - URL: `/tts`
   - Method: POST
   - Headers:
     - `X-App-ID`: Your App ID
     - `X-App-Key`: Your App Key
   - Body: JSON
     ```json
     {
       "text": "Your text to convert to speech"
     }
     ```

3. **Debug Audio**
   - URL: `/debug_audio`
   - Method: GET
   - Headers:
     - `X-App-ID`: Your App ID
     - `X-App-Key`: Your App Key

## Docker Deployment

To build and run the Docker container:

```
docker build -t stt-tts-api .
docker run -p 8000:8000 stt-tts-api
```

## Configuration

Set the following environment variables:
- `APP_ID`: Your application ID
- `APP_KEY`: Your application key

## Logging

Logs are configured to output to the console with INFO level. Check the logs for debugging and monitoring the application's behavior.

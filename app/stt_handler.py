import speech_recognition as sr
from io import BytesIO
import logging
import wave

logger = logging.getLogger(__name__)

def speech_to_text(audio_content: bytes) -> str:
    recognizer = sr.Recognizer()
    
    try:
        # Log audio content details
        logger.info(f"Received audio content of size: {len(audio_content)} bytes")
        
        # Try to open the audio as a WAV file and log its properties
        try:
            with wave.open(BytesIO(audio_content), 'rb') as wav_file:
                logger.info(f"WAV file properties: channels={wav_file.getnchannels()}, "
                            f"sample_width={wav_file.getsampwidth()}, "
                            f"framerate={wav_file.getframerate()}, "
                            f"n_frames={wav_file.getnframes()}")
        except wave.Error:
            logger.warning("Couldn't open audio as WAV file. It might be in a different format.")

        with sr.AudioFile(BytesIO(audio_content)) as source:
            logger.info("Reading audio file")
            audio = recognizer.record(source)
        
        logger.info("Recognizing speech")
        text = recognizer.recognize_google(audio)
        logger.info(f"Speech recognized: {text}")
        return text
    except ValueError as e:
        logger.error(f"Error reading audio file: {str(e)}")
        raise ValueError("Audio file could not be read. Please ensure it's in WAV, AIFF, or FLAC format.")
    except sr.UnknownValueError:
        logger.warning("Speech recognition could not understand the audio")
        return "Speech recognition could not understand the audio"
    except sr.RequestError as e:
        logger.error(f"Could not request results from speech recognition service: {str(e)}")
        return f"Could not request results from speech recognition service; {e}"
    except Exception as e:
        logger.error(f"Unexpected error in speech recognition: {str(e)}")
        raise

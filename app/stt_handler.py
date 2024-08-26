import speech_recognition as sr
from io import BytesIO
import logging

logger = logging.getLogger(__name__)

def speech_to_text(audio_content: bytes) -> str:
    recognizer = sr.Recognizer()
    
    try:
        with sr.AudioFile(BytesIO(audio_content)) as source:
            logger.info("Reading audio file")
            audio = recognizer.record(source)
        
        logger.info("Recognizing speech")
        text = recognizer.recognize_google(audio)
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

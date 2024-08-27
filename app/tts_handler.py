import logging
import io
from gtts import gTTS
import base64

logger = logging.getLogger(__name__)

def text_to_speech(text: str) -> str:
    try:
        logger.info(f"Starting text_to_speech function with text: {text[:50]}...")

        audio_buffer = io.BytesIO()
        tts = gTTS(text=text, lang='en')
        tts.write_to_fp(audio_buffer)
        logger.info(f"Generated audio. Buffer size: {audio_buffer.getbuffer().nbytes} bytes")

        audio_buffer.seek(0)
        audio_data = audio_buffer.getvalue()
        base64_audio = base64.b64encode(audio_data).decode('utf-8')
        logger.info(f"Encoded audio to base64. Length: {len(base64_audio)}")

        return base64_audio
    except Exception as e:
        logger.error(f"Error in text_to_speech: {str(e)}", exc_info=True)
        raise
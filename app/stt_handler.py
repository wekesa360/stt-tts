import logging
import io
import speech_recognition as sr
import wave
from pydub import AudioSegment

logger = logging.getLogger(__name__)

def convert_to_pcm_wav(audio_file):
    try:
        audio = AudioSegment.from_file(audio_file)
        logger.info("Successfully read audio file")
    except Exception as e:
        logger.warning(f"Couldn't read audio file directly: {str(e)}")
        try:
            audio_file.seek(0)
            audio = AudioSegment.from_raw(audio_file, sample_width=2, frame_rate=16000, channels=1)
            logger.info("Successfully read audio file as raw PCM data")
        except Exception as e:
            logger.error(f"Failed to read audio file as raw PCM data: {str(e)}", exc_info=True)
            raise

    pcm_wav_io = io.BytesIO()
    audio.export(pcm_wav_io, format="wav", parameters=["-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1"])
    pcm_wav_io.seek(0)
    logger.info("Converted audio to PCM WAV format")
    return pcm_wav_io

def speech_to_text(audio_file):
    recognizer = sr.Recognizer()
    
    try:
        pcm_wav_io = convert_to_pcm_wav(audio_file)
        
        with wave.open(pcm_wav_io, 'rb') as wav_file:
            logger.info(f"WAV file properties: channels={wav_file.getnchannels()}, "
                        f"sample_width={wav_file.getsampwidth()}, "
                        f"framerate={wav_file.getframerate()}, "
                        f"n_frames={wav_file.getnframes()}")
        
        pcm_wav_io.seek(0)

        with sr.AudioFile(pcm_wav_io) as source:
            logger.info("Reading audio data")
            audio_data = recognizer.record(source)

        logger.info("Recognizing speech")
        text = recognizer.recognize_google(audio_data)
        logger.info(f"Speech recognized: {text}")
        return text
    except sr.UnknownValueError:
        logger.warning("Speech recognition could not understand the audio")
        return "Speech recognition could not understand the audio"
    except sr.RequestError as e:
        logger.error(f"Could not request results from speech recognition service: {str(e)}", exc_info=True)
        return f"Could not request results from speech recognition service; {e}"
    except Exception as e:
        logger.error(f"Unexpected error in speech recognition: {str(e)}", exc_info=True)
        raise
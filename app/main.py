import logging
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.security import APIKeyHeader
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel
from auth import verify_api_key
from stt_handler import speech_to_text
from tts_handler import text_to_speech
import io
import magic
import numpy as np
import soundfile as sf
from transformers import pipeline


# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI()
APP_ID = APIKeyHeader(name="X-App-ID")
APP_KEY = APIKeyHeader(name="X-App-Key")


class TextInput(BaseModel):
    text: str


# Initialize the translation pipelines
sw_to_en = pipeline("translation", model="Bildad/Swahili-English_Translation")
en_to_sw = pipeline("translation", model="Bildad/English-Swahili_Translation")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/stt")
async def stt_endpoint(
    request: Request, app_id: str = Depends(APP_ID), app_key: str = Depends(APP_KEY)
):
    if not verify_api_key(app_id, app_key):
        logger.warning("Invalid API Key attempt")
        raise HTTPException(status_code=401, detail="Invalid API Key")

    content_type = request.headers.get("Content-Type", "")
    logger.info(f"Received request with Content-Type: {content_type}")

    try:
        audio_content = await request.body()
        logger.info(f"Audio content size: {len(audio_content)} bytes")

        audio_io = io.BytesIO(audio_content)
        audio_io.name = "audio.wav"

        file_type = magic.from_buffer(audio_content, mime=True)
        logger.info(f"Determined file type: {file_type}")

        text = speech_to_text(audio_io)
        return {"text": text}
    except ValueError as e:
        logger.error(f"Error processing audio: {str(e)}", exc_info=True)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/tts")
async def tts_endpoint(
    input: TextInput, app_id: str = Depends(APP_ID), app_key: str = Depends(APP_KEY)
):
    if not verify_api_key(app_id, app_key):
        logger.warning("Invalid API Key attempt")
        raise HTTPException(status_code=401, detail="Invalid API Key")
    logger.info(f"Received TTS request with text: {input.text[:50]}...")
    try:
        base64_audio = text_to_speech(input.text)
        logger.info(f"Successfully generated audio. Base64 length: {len(base64_audio)}")
        return {"audio": base64_audio}
    except Exception as e:
        logger.error(f"Error in TTS endpoint: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/debug_audio")
async def debug_audio_endpoint(
    app_id: str = Depends(APP_ID), app_key: str = Depends(APP_KEY)
):
    if not verify_api_key(app_id, app_key):
        logger.warning("Invalid API Key attempt")
        raise HTTPException(status_code=401, detail="Invalid API Key")
    try:
        sample_rate = 44100
        duration = 3
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        audio = np.sin(440 * 2 * np.pi * t)
        audio = (audio * 32767).astype(np.int16)

        buffer = io.BytesIO()
        sf.write(buffer, audio, sample_rate, format="WAV")
        buffer.seek(0)

        logger.info("Successfully generated debug audio")
        return StreamingResponse(buffer, media_type="audio/wav")
    except Exception as e:
        logger.error(f"Error generating debug audio: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error generating debug audio")


class TranslationInput(BaseModel):
    text: str
    target: str


@app.post("/translate")
async def translate_endpoint(
    input: TranslationInput,
):
    text_to_translate = input.text
    target_language = input.target

    logger.info(
        f"Received translation request: '{text_to_translate[:50]}' to {target_language}"
    )

    if target_language == "sw":
        translation = en_to_sw(text_to_translate)[0]
    elif target_language == "en":
        translation = sw_to_en(text_to_translate)[0]
    else:
        logger.warning(f"Invalid target language: {target_language}")
        raise HTTPException(status_code=400, detail="Invalid Target Language")

    translated_text = translation["translation_text"]
    logger.info(
        f"Successfully translated text to {target_language}: {translated_text[:50]}"
    )

    return JSONResponse(content={"translated_text": translated_text})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

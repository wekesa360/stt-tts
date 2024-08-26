import logging
from fastapi import FastAPI, Depends, HTTPException, File, UploadFile
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from auth import verify_api_key
from stt_handler import speech_to_text
from tts_handler import text_to_speech

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
APP_ID = APIKeyHeader(name="X-App-ID")
APP_KEY = APIKeyHeader(name="X-App-Key")

class TextInput(BaseModel):
    text: str

@app.post("/stt")
async def stt_endpoint(
    file: UploadFile = File(...),
    app_id: str = Depends(APP_ID),
    app_key: str = Depends(APP_KEY)
):
    if not verify_api_key(app_id, app_key):
        raise HTTPException(status_code=401, detail="Invalid API Key")
    
    logger.info(f"Received file: {file.filename}, content_type: {file.content_type}")
    
    try:
        audio_content = await file.read()
        logger.info(f"Audio content size: {len(audio_content)} bytes")
        
        text = speech_to_text(audio_content)
        return {"text": text}
    except ValueError as e:
        logger.error(f"Error processing audio: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/tts")
async def tts_endpoint(
    input: TextInput,
    app_id: str = Depends(APP_ID),
    app_key: str = Depends(APP_KEY)
):
    if not verify_api_key(app_id, app_key):
        raise HTTPException(status_code=401, detail="Invalid API Key")
    
    audio_content = text_to_speech(input.text)
    return {"audio": audio_content}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    

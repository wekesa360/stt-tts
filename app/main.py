from fastapi import FastAPI, Depends, HTTPException, File, UploadFile
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from auth import verify_api_key
from stt_handler import speech_to_text
from tts_handler import text_to_speech

app = FastApi()

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

    audio_content = await file.read()
    text = speech_to_text(audio_content)
    return {"text": text}

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
    
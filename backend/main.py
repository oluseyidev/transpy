import base64
from fastapi import FastAPI, Body, Request
from services.azure_tts import synthesize_speech
from services.azure_stt import transcribe_speech
from fastapi.responses import JSONResponse
from services.translate import translate_text
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/translate/")
async def translate(data: dict = Body(...)):
    text = data["text"]
    to_lang = data["to_lang"]
    result = await translate_text(text, to_lang)
    return {"translated_text": result}

@app.post("/speak/")
async def speak(data: dict = Body(...)):
    text = data["text"]
    language = data["language"]
    audio_base64 = synthesize_speech(text, language)
    return {"audio_base64": audio_base64}

@app.post("/speech-to-text/")
async def speech_to_text(request: Request):
    try:
        content_type = request.headers.get("Content-Type", "")
        
        if content_type == "application/json":
            payload = await request.json()
            audio_data = payload["audio_base64"]
            language = payload.get("language", "en-US")
        else:  # Assume raw audio
            audio_data = base64.b64encode(await request.body()).decode("utf-8")
            language = request.headers.get("Language", "en-US")
            
        text = transcribe_speech(audio_data, language)
        return {"transcribed_text": text}
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})

from pydub import AudioSegment
import azure.cognitiveservices.speech as speechsdk
import os
import base64
import tempfile


def transcribe_speech(audio_base64: str, language: str = "en-US") -> str:
    key = os.getenv("AZURE_SPEECH_KEY")
    region = os.getenv("AZURE_SPEECH_REGION")

    audio_data = base64.b64decode(audio_base64)

    # Save MP3 to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as mp3_file:
        mp3_file.write(audio_data)
        mp3_path = mp3_file.name

    # Convert MP3 to WAV (PCM 16-bit mono 16kHz)
    wav_path = mp3_path.replace(".mp3", ".wav")
    sound = AudioSegment.from_mp3(mp3_path)
    sound = sound.set_channels(1).set_frame_rate(16000).set_sample_width(2)
    sound.export(wav_path, format="wav")

    print(f"[DEBUG] Converted WAV path: {wav_path}")

    # Configure Azure STT
    speech_config = speechsdk.SpeechConfig(subscription=key, region=region)
    speech_config.speech_recognition_language = language
    audio_config = speechsdk.audio.AudioConfig(filename=wav_path)

    recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config,
        audio_config=audio_config
    )

    result = recognizer.recognize_once()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return result.text
    elif result.reason == speechsdk.ResultReason.NoMatch:
        raise Exception("No speech could be recognized.")
    else:
        raise Exception(f"Speech recognition error: {result.reason} — {result.cancellation_details.error_details}")

import azure.cognitiveservices.speech as speechsdk
from azure.cognitiveservices.speech import (SpeechConfig, SpeechSynthesizer, AudioConfig)
from transformers import pipeline
from scipy.io.wavfile import write as wav_write
import tempfile
import base64
import torch
import os
import numpy as np
import soundfile as sf


class AudioBufferCallback(speechsdk.audio.PushAudioOutputStreamCallback):
    def __init__(self):
        super().__init__()
        self._buffer = bytearray()

    def write(self, audio_buffer: memoryview) -> int:
        self._buffer.extend(audio_buffer)
        return audio_buffer.nbytes

    def close(self):
        pass

    def get_buffer(self):
        return bytes(self._buffer)

def synthesize_speech_azure(text, lang="en-US"):
    key = os.getenv("AZURE_SPEECH_KEY")
    region = os.getenv("AZURE_SPEECH_REGION")

    speech_config = SpeechConfig(subscription=key, region=region)
    speech_config.speech_synthesis_language = lang
    # speech_config.speech_synthesis_voice_name = f"{lang}-Neural"
    # speech_config.speech_synthesis_voice_name = "en-NG-AbeoNeural"
    speech_config.speech_synthesis_voice_name = "en-NG-EzinneNeural"

    # ✅ Make the audio browser-compatible
    speech_config.set_speech_synthesis_output_format(
        speechsdk.SpeechSynthesisOutputFormat.Audio24Khz160KBitRateMonoMp3
    )


    # Set up push audio stream with callback
    callback = AudioBufferCallback()
    push_stream = speechsdk.audio.PushAudioOutputStream(callback)
    audio_config = AudioConfig(stream=push_stream)
    synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    # Trigger synthesis
    result = synthesizer.speak_text_async(text).get()

    if result.reason == speechsdk.ResultReason.Canceled:
        cancellation = speechsdk.CancellationDetails.from_result(result)
        print(f"[ERROR] Canceled: {cancellation.reason}")
        if cancellation.reason == speechsdk.CancellationReason.Error:
            print(f"[ERROR] Error details: {cancellation.error_details}")
        raise Exception(f"Speech synthesis canceled: {cancellation.error_details}")

    if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
        raise Exception(f"Speech synthesis failed: {result.reason}")


    audio_buffer = callback.get_buffer()
    if not audio_buffer:
        raise Exception("No audio data received")
    
    with open("test_output.mp3", "wb") as f:
        f.write(audio_buffer)

    print(f"[DEBUG] Final audio length: {len(audio_buffer)} bytes")

    return base64.b64encode(audio_buffer).decode("utf-8")

def synthesize_speech(text: str, lang_code: str = "yor") -> str:
    print(f"[TTS] Synthesizing for '{text}' in language '{lang_code}'...")

    model_id = f"facebook/mms-tts-{lang_code}"
    tts = pipeline("text-to-speech", model=model_id)

    output = tts(text)
    audio = output["audio"]  # NumPy float32 array
    sampling_rate = output["sampling_rate"]

    # 🛠 Fix: ensure it's 1D float32
    audio = np.asarray(audio, dtype=np.float32).flatten()

    # 🛠 Fix: Write as raw PCM 16-bit WAV
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
        sf.write(tmp_file.name, audio, sampling_rate, format="WAV", subtype="PCM_16")
        tmp_path = tmp_file.name
    print(f"[TTS] Audio saved to: {tmp_path}")
    
    with open(tmp_path, "rb") as f:
        audio_base64 = base64.b64encode(f.read()).decode("utf-8")

    os.remove(tmp_path)
    return audio_base64

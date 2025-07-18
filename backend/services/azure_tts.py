import azure.cognitiveservices.speech as speechsdk
from azure.cognitiveservices.speech import (
    SpeechConfig, SpeechSynthesizer, AudioConfig
)
import base64
import os

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

def synthesize_speech(text, lang="en-US"):
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

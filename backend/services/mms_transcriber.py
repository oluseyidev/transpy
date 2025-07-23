import torch
from transformers import AutoProcessor, Wav2Vec2ForCTC


MMS_MODEL_ID = "facebook/mms-1b-all"
def transcribe_with_mms(audio_array, lang_code, sampling_rate=16000):
    print(f"[MMS] Loading processor and model for: {lang_code}")
    
    print("[MMS] Loading processor...")
    processor = AutoProcessor.from_pretrained(MMS_MODEL_ID, target_lang=lang_code)
    print("[MMS] Processor loaded successfully")
    
    print("[MMS] Loading model...")
    model = Wav2Vec2ForCTC.from_pretrained(
        MMS_MODEL_ID,
        target_lang=lang_code,
        ignore_mismatched_sizes=True,
    )
    print("[MMS] Model loaded successfully")
    
    print("[MMS] Setting model to eval mode...")
    model.eval()
    
    print("[MMS] Processing audio input...")
    inputs = processor(audio_array, sampling_rate=sampling_rate, return_tensors="pt")
    print("[MMS] Audio processed successfully")
    
    print("[MMS] Running inference...")
    with torch.no_grad():
        logits = model(**inputs).logits
    print("[MMS] Inference completed")
    
    print("[MMS] Decoding output...")
    predicted_ids = torch.argmax(logits, dim=-1)[0]
    transcription = processor.decode(predicted_ids)
    
    print(f"[MMS] Final Transcription: {transcription}")
    return transcription.lower()

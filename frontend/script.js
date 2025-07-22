let currentTranslatedText = '';
let selectedLang = '';

async function translateText() {
  const inputText = document.getElementById("inputText").value;
  selectedLang = document.getElementById("languageSelect").value;

  const res = await fetch("http://127.0.0.1:8000/translate/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      text: inputText,
      to_lang: selectedLang
    })
  });

  const data = await res.json();
  currentTranslatedText = data.translated_text;
  document.getElementById("outputText").innerText = currentTranslatedText;
}

async function playAudio() {
  if (!currentTranslatedText) return alert("Translate something first!");

  const res = await fetch("http://127.0.0.1:8000/speak/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      text: currentTranslatedText,
      language: selectedLang
    })
  });

  const data = await res.json();
  const audioBase64 = data.audio_base64;

  if (!audioBase64) {
    console.error("No audio data returned.");
    return;
  }

  // ✅ Construct Data URI
  const audioUrl = `data:audio/mpeg;base64,${audioBase64}`;
  const audio = new Audio(audioUrl);
  console.log(audioUrl);

  audio.addEventListener("error", (e) => {
    console.error("Audio load/play error:", e);
  });

  audio.play().catch(err => {
    console.error("Play error:", err);
  });
}


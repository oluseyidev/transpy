import os
import httpx
from dotenv import load_dotenv

load_dotenv()

async def translate_text(text, to_lang="en", from_lang="yo"):
    endpoint = os.getenv("AZURE_TRANSLATOR_ENDPOINT")
    key = os.getenv("AZURE_TRANSLATOR_KEY")

    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Ocp-Apim-Subscription-Region": "eastus2",
        "Content-type": "application/json",
    }

    # Map 'ib' to 'ig' for language codes
    lang_map = {"ib": "ig"}
    from_lang_code = lang_map.get(from_lang[:2], from_lang[:2])
    to_lang_code = lang_map.get(to_lang[:2], to_lang[:2])
    print(f"[DEBUG] Translating '{text}' from '{from_lang_code}' to '{to_lang_code}'...")
    params = {"api-version": "3.0", "from": from_lang_code, "to": to_lang_code}
    body = [{"text": text}]

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{endpoint}/translate",
            headers=headers,
            params=params,
            json=body
        )
        response.raise_for_status()
        return response.json()[0]["translations"][0]["text"]

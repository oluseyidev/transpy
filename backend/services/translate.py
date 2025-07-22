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
    print(f"[DEBUG] Translating '{text}' from '{from_lang[:2]}' to '{to_lang[:2]}'...")
    params = {"api-version": "3.0", "from": from_lang[:2], "to": to_lang[:2]}
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

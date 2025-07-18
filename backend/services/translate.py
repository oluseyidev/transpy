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

    params = {"api-version": "3.0", "from": from_lang, "to": to_lang}
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

import requests
import uuid
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "mistral"

def call_ollama(prompt: str) -> str:
    response = requests.post(OLLAMA_URL, json={
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    })
    return response.json()["response"].strip()

def mask_pii(text: str):
    prompt = (
        "The following text contains personal information. "
        "Identify all PII (like names, emails, phone numbers, SSNs, addresses, etc.) "
        "and replace them with fake placeholders like <MASK_1>, <MASK_2>, etc. "
        "Then return both:\n\n"
        "1. The masked version of the text\n"
        "2. A JSON mapping of each <MASK_x> to the original value.\n\n"
        f"Text:\n{text}\n"
    )

    response = call_ollama(prompt)

    # Attempt to extract masked text and mapping from model's response
    try:
        masked_part, mapping_part = response.split("2.", 1)
        masked_text = masked_part.replace("1.", "").strip()
        mapping_json = mapping_part.strip()

        pii_map = json.loads(mapping_json)
        return masked_text, pii_map
    except Exception as e:
        print("Failed to parse model response. Full response below:\n")
        print(response)
        raise e


def restore_original_text(masked_text: str, pii_mapping: dict) -> str:
    restored_text = masked_text
    for mask, original in pii_mapping.items():
        restored_text = restored_text.replace(mask, original)
    return restored_text


def main():
    text = "Pedro é um cidadão com CNH 152.526.266-11 que gosta de ir ao cinema. Seu email é pedrolinhares@gmail.com"
    masked_text, pii_mapping = mask_pii(text)

    # Save mapping to file with unique name
    map_file = f"pii_mapping_{uuid.uuid4().hex[:8]}.json"
    with open(map_file, "w") as f:
        json.dump(pii_mapping, f, indent=2)

    restored = restore_original_text(masked_text, pii_mapping)

    print("\n✅ Masked Text:\n", masked_text)
    print(f"\n📁 PII mapping saved to: {map_file}")
    print(f"\n🔍 Restored Text:\n{restored}")

if __name__ == "__main__":
    main()

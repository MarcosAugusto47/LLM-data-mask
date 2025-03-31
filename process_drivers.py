
import json
import tqdm
from llm_data_mask import process_driver_text, mask_pii, unmask_pii


def main():
    # Read input data
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    data = data[:5]

    # Process each sample
    results = []
    for item in tqdm.tqdm(data, desc="Processing samples"):
        if isinstance(item, dict) and 'text' in item:
            mapping, masked_text, processed_text = process_driver_text(item['text'])

            # print("Mapping")
            # print(mapping)
            # print("\n")

            # # Mask PII information
            # print("Masking PII information")
            # masked_text = mask_pii(driver_details, mapping)

            # print(masked_text)
            # print("\n")

            # # Unmask PII information
            # print("Unmasking PII information")
            # unmasked_text = unmask_pii(masked_text, mapping)
            # print(unmasked_text)
            print(item['text'])
            print(mapping)

            masked_text = mask_pii(item['text'], mapping)

            if masked_text:
                results.append({
                    'original': item,
                    'masked_text': masked_text
                })
    
    # Save results
    output_file = 'extracted_data.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"Processed {len(results)} samples. Results saved to {output_file}")


if __name__ == "__main__":
    main() 
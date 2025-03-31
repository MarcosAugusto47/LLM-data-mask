from llm_data_mask import process_driver_text, mask_pii, unmask_pii

# This completely fake data is used to demonstrate the model's capabilities
driver_details = "abc xyz 123"

mapping, masked_text, processed_text = process_driver_text(driver_details)

print("Mapping")
print(mapping)
print("\n")

# Mask PII information
print("Masking PII information")
masked_text = mask_pii(driver_details, mapping)

print(masked_text)
print("\n")

# Unmask PII information
print("Unmasking PII information")
unmasked_text = unmask_pii(masked_text, mapping)
print(unmasked_text)

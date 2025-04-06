from llm_data_mask import process_driver_text, mask_pii, unmask_pii, check_mapping

# This completely fake data is used to demonstrate the model's capabilities
# driver_details = "FELIPE SANTANA SOUZA ANDRE, brasileiro, professor, portador da cédula de identidade RG 2412197 SSP/DF, CPF n. 014.352.181-08, residente e domiciliado na SQSW 105, BL A, APT 301, Setor Sudoeste, Brasília - DF, Brasil, CEP: 70.670-421, celular: (61) 9 9966-7754"

driver_details = """
LEONARDO HENRIQUE MAGALHAES DE OLIVEIRA, brasileiro, advogado, portador da cédula de identidade RG 1259300 SSP/DF, CPF n. 647.882.451-91, residente e domiciliado no SHS Quadra 06, Bloco C, 513, Ed. Brasil 21, DF - Brasília, CEP: 70.316-109, celular: (61) 9 9297-5656
"""

mapping, masked_text, processed_text = process_driver_text(driver_details)

print("Mapping")
print(mapping)
print("\n")

# Mask PII information
print("Masking PII information")
print(masked_text)
print("\n")

# Unmask PII information
print("Unmasking PII information")
unmasked_text = unmask_pii(masked_text, mapping)
print(unmasked_text)

# check_mapping(mapping, driver_details)

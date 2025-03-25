import outlines
from pydantic import BaseModel, Field

from helpers import (
    fix_comma_spacing_regex,
    mask_pii,
    remove_extra_spaces_regex,
    unmask_pii,
)


class DriverDetails(BaseModel):
    name: str = Field(pattern=r"([A-Z]+ ?)+")
    RG: str = Field(pattern=r"[0-9-]*")  # Added hyphen to allow RG with hyphens
    CPF: str = Field(
        pattern=r"[0-9.-]+"
    )  # Added hyphen to allow CPF with dots and hyphens
    address: str
    CEP: str = Field(
        pattern=r"[0-9.-]*"
    )  # Added hyphen to allow CEP with hyphens
    phonenumber: str = Field(
        pattern=r"^[\d\-\(\)\s]+$"
    )  # Added hyphen to allow phonenumber with hyphens


# model = outlines.models.transformers("microsoft/Phi-4-mini-instruct")
# model = outlines.models.transformers("microsoft/phi-1_5")
# model = outlines.models.transformers("HuggingFaceTB/SmolLM2-1.7B-Instruct")
# model = outlines.models.transformers("Qwen/Qwen1.5-0.5B")
# model = outlines.models.transformers("Qwen/Qwen1.5-1.8B")
model = outlines.models.transformers("Qwen/Qwen2.5-1.5B")

# Construct structured sequence generator
generator = outlines.generate.json(model, DriverDetails)

# This completely fake data is used to demonstrate the model's capabilities
driver_details = "MATHEUS PAULO MENDES, brasileiro, advogado, portador do RG n.° 456536899 SSP/SP, CPF n. 910.298.270-60, residente e domiciliado na Rua 04 Oeste, lote 06 Bloco G, apto 303, Residencial Serenidade, Águas Correntes, Ouro Preto - MG, Brasil, CEP 69095-614, celular (92) 99625-2343"

driver_details = remove_extra_spaces_regex(driver_details)
driver_details = fix_comma_spacing_regex(driver_details)

# This completely fake data is used to demonstrate the model's capabilities
prompt = f"""
Extract the details of the driver for the provided text.

Keep in mind that the address field is everything after the CPF number and before the phone number, do not change the sequence of the information to be extracted.

Example 1
Input
PAULO GIOVANI LEANDRO DIAS, brasileiro, comerciante, portador da cédula de identidade RG 324830130 SSP/DF, CPF n. 802.881.025-09, residente e domiciliado na Avenida Joaquim Coutinho, 201, Marabaixo, Macapá - AP, CEP 68906-491, celular (96) 98226-8422

Output
name: PAULO GIOVANI LEANDRO DIAS
RG: 324830130 SSP/DF
CPF: 802.881.025-09
address: Avenida Joaquim Coutinho, 201, Marabaixo, Macapá - AP
CEP: 68906-491
phonenumber: (96) 98226-8422


Example 2
Input
LAURA SOPHIA JOSEFA BARBOSA, brasileira, consultora de vendas, portadora do RG n.° 209668283 SSP/DF, CPF n. 709.506.304-46, residente e domiciliado na Av. Liberdade, Lotes 04/17, Quadra 204, Bloco M, Apt. 102, St Ivo, Santa Cecília-DF, CEP 76816-800, celular (61) 9 9133-5265

Output
name: LAURA SOPHIA JOSEFA BARBOSA
RG: 209668283 SSP/DF
CPF: 709.506.304-46
address: Av. Liberdade, Lotes 04/17, Quadra 204, Bloco M, Apt. 102, St Ivo, Santa Cecília - DF
CEP: 76816-800
phonenumber: (61) 9 9133-5265

Your Input
{driver_details}

Your Output
"""

mapping = generator(prompt)

mapping = mapping.model_dump()

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

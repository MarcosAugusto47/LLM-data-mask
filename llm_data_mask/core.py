import outlines
from pydantic import BaseModel, Field

from .helpers import (
    fix_comma_spacing_regex,
    mask_pii,
    remove_extra_spaces_regex,
)


class DriverDetails(BaseModel):
    name: str = Field(pattern=r"([A-Z]+ ?)+")
    RG: str = Field(
        pattern=r"[0-9.-]*"
    )  # Added hyphen to allow RG with hyphens
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


def extract_driver_details(driver_details_text):
    """
    Extract driver details from text using a language model.

    Args:
        driver_details_text (str): The text containing driver details

    Returns:
        dict: Extracted driver details
    """
    # Preprocess the text
    driver_details_text = remove_extra_spaces_regex(driver_details_text)
    driver_details_text = fix_comma_spacing_regex(driver_details_text)

    # Initialize the model
    # model = outlines.models.transformers("Qwen/Qwen2.5-1.5B")
    model = outlines.models.transformers("Qwen/Qwen2.5-1.5B-Instruct")
    # model = outlines.models.transformers("Qwen/Qwen2.5-3B-Instruct") # this model takes too long to run

    # Construct structured sequence generator
    generator = outlines.generate.json(model, DriverDetails)

    # Create the prompt
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
    CEP: 68906-491
    phonenumber: (96) 98226-8422
    address: Avenida Joaquim Coutinho, 201, Marabaixo, Macapá - AP

    
    Example 2
    Input
    portadora do RG n.° 209668283 SSP/DF, LAURA SOPHIA JOSEFA BARBOSA, brasileira, celular (61) 9 9133-5265, consultora de vendas, CPF n. 709.506.304-46, residente e domiciliado na Av. Liberdade, Lotes 04/17, Quadra 204, Bloco M, Apt. 102, St Ivo, Santa Cecília-DF, CEP 76816-800

    Output
    name: LAURA SOPHIA JOSEFA BARBOSA
    RG: 209668283 SSP/DF
    CPF: 709.506.304-46
    CEP: 76816-800
    phonenumber: (61) 9 9133-5265
    address: Av. Liberdade, Lotes 04/17, Quadra 204, Bloco M, Apt. 102, St Ivo, Santa Cecília - DF

    
    Example 3
    Input
    GUSTAVO FELIPE ASSUNÇÃO, brasileiro, funcionário público, portador da cédula de identidade RG 251143922 SSP/CE, CPF n. 733.584.223-99, residente e domiciliado na Rua do Gelo, 453, Edson Queiroz, Fortaleza - CE, Brasil, CEP: 60812-180, celular: (85) 98236-2345

    Output
    name: GUSTAVO FELIPE ASSUNÇÃO
    RG: 251143922 SSP/CE
    CPF: 733.584.223-99
    CEP: 60812-180
    phonenumber: (85) 98236-2345
    address: Rua do Gelo, 453, Edson Queiroz, Fortaleza - CE, Brasil

    
    Example 4
    Input
    EVELYN LÍVIA PEREIRA, brasileira, supervisora administrativo, portadora da cédula de identidade RG 356640061 SSP/SP, CPF n. 516.692.173-96, residente e domiciliado no Rua C, 706, Canindezinho, São Paulo - SP, Brasil, CEP: 60733-017, celular: (12) 99293-3582, vem respeitosamente à presença de Vossa Senhoria, através de seus procuradores (procuração anexa), interpor RECURSO À JARI - SUSPENSÃO DO DIREITO DE DIRIGIR

    Output
    name: EVELYN LÍVIA PEREIRA
    RG: 356640061 SSP/SP
    CPF: 516.692.173-96
    CEP: 60733-017
    phonenumber: (12) 99293-3582
    address: Rua C, 706, Canindezinho, São Paulo - SP, Brasil
    

    Example 5
    Input
    BRENO YURI EDSON VIANA, brasileiro, servidor público, portadora do RG n.° 362063278 SSP/DF, CPF n. 966.388.721-41, residente e domiciliado na Quadra SQN 314 Bloco F, 898, Asa Norte, Brasília - DF, Brasil, CEP 70767-060, celular (61) 98397-5024, vem respeitosamente à presença de Vossa Senhoria, através de seus procuradores (procuração anexa), apresentar RECURSO À JARI - SUSPENSÃO DO DIREITO DE DIRIGIR Com base no artigo 265 do Código de Trânsito Brasileiro, conforme notificação anexa, o que faz da seguinte forma:

    Output
    name: BRENO YURI EDSON VIANA
    RG: 362063278 SSP/DF
    CPF: 966.388.721-41
    CEP: 70767-060
    phonenumber: (61) 98397-5024
    address: Quadra SQN 314 Bloco F, 898, Asa Norte, Brasília - DF, Brasil
    

    Your Input
    {driver_details_text}

    Your Output
    """

    # Generate the mapping
    mapping = generator(prompt)

    # Convert to dictionary
    return mapping.model_dump()


def process_driver_text(text):
    """
    Process driver text by extracting details, masking PII, and returning both masked and original.

    Args:
        text (str): The text containing driver details

    Returns:
        tuple: (extracted_details, masked_text, original_text)
    """
    # Preprocess the text
    processed_text = remove_extra_spaces_regex(text)
    processed_text = fix_comma_spacing_regex(processed_text)

    # Extract driver details
    mapping = extract_driver_details(processed_text)

    # Mask PII information
    masked_text = mask_pii(processed_text, mapping)

    return mapping, masked_text, processed_text

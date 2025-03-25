import outlines
from pydantic import BaseModel, Field

from .helpers import (
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
    model = outlines.models.transformers("Qwen/Qwen2.5-1.5B")
    
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

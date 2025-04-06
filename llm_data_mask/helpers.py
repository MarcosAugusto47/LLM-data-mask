import re


def mask_pii(text, pii_dict, mask_format="[{pii_type}]"):
    """
    Masks PII information in text based on a dictionary of identified PII elements.
    
    Args:
        text (str): The original text containing PII information
        pii_dict (dict): A dictionary where keys are PII types and values are the actual PII values
                         Example: {"NAME": "John Doe", "EMAIL": "john@example.com", "SSN": "123-45-6789"}
        mask_format (str): Format string for the mask, with {pii_type} as a placeholder
                          Default is "[{pii_type}]", which will replace "John Doe" with "[NAME]"
    
    Returns:
        str: The text with PII information masked
    """
    masked_text = text
    
    # Sort PII elements by length (descending) to avoid partial replacements
    # For example, replace "John Doe" before "John" if both are in the dictionary
    all_pii_items = []
    for pii_type, value in pii_dict.items():
        # Skip None values or non-string values
        if value is None or not isinstance(value, str):
            continue
        all_pii_items.append((value, pii_type))
    
    # Sort by length (longest first)
    all_pii_items.sort(key=lambda x: len(x[0]), reverse=True)
    # Replace each PII item with its mask

    for pii_item, pii_type in all_pii_items:
        
        mask = mask_format.format(pii_type=pii_type)
        
        if pii_item in masked_text:
            masked_text = masked_text.replace(pii_item, mask)
        else:
            print(f"'{pii_item}' not found in text.")        
            # Apply additional masking for specific patterns
            masked_text = replace_if_matches_ends(masked_text, pii_item, mask)
    
    return masked_text


def unmask_pii(masked_text, pii_dict, mask_format="[{pii_type}]"):
    """
    Replaces masked PII elements in text with their original values using a PII dictionary.
    
    Args:
        masked_text (str): The text with masked PII information
        pii_dict (dict): A dictionary where keys are PII types and values are the actual PII values
                        Example: {"NAME": "John Smith", "EMAIL": "john.smith@example.com"}
        mask_format (str): The format string that was used for masking, with {pii_type} as placeholder
                          Default is "[{pii_type}]", which will replace "[NAME]" with "John Smith"
    
    Returns:
        str: The text with PII information restored
    """
    unmasked_text = masked_text
    
    # Create a mapping of mask to original value
    masks_to_values = {}
    for pii_type, value in pii_dict.items():
        # Skip None values or non-string values
        if value is None or not isinstance(value, str):
            continue
        
        # Create the mask using the provided format
        mask = mask_format.format(pii_type=pii_type)
        masks_to_values[mask] = value
    
    # Replace each mask with its original value
    for mask, original_value in masks_to_values.items():
        unmasked_text = unmasked_text.replace(mask, original_value)
    
    return unmasked_text


def remove_dots_and_hyphens(input_string):
    """
    Removes all dots (.) and hyphens (-) from a string.
    
    Args:
        input_string (str): The string to process
        
    Returns:
        str: The string with all dots and hyphens removed
    """
    # Replace dots and hyphens with an empty string
    result = input_string.replace('.', '').replace('-', '')
    return result


def fix_comma_spacing_regex(input_string):
    """
    Ensures that commas come right after a character or digit, not after whitespace.
    Uses regex to replace any whitespace followed by a comma with just a comma.
    
    Args:
        input_string (str): The string to process
        
    Returns:
        str: The string with properly positioned commas
    """
    if not input_string:
        return input_string
    
    # Replace any whitespace followed by a comma with just a comma
    return re.sub(r'\s+,', ',', input_string)


def remove_extra_spaces_regex(input_string):
    """
    Removes multiple consecutive blank spaces, replacing them with a single space.
    
    Args:
        input_string (str): The string to process
        
    Returns:
        str: The string with consecutive spaces replaced by a single space
    """
    if not input_string:
        return input_string
    
    # Replace one or more whitespace characters with a single space
    return re.sub(r'\s+', ' ', input_string)


def replace_if_matches_ends(original_string, comparison_string, replacement, end_length=3):
    """
    Replace all substrings in the original_string if they start with the first part
    and end with the last part of the comparison_string.
    
    Args:
        original_string: The string to be modified
        comparison_string: The string whose ends we're checking against
        replacement: What to replace matching substrings with
        end_length: Length of the prefix and suffix to match (default=3)
    
    Returns:
        Modified original_string with all matches replaced
    """
    if not comparison_string or len(comparison_string) < end_length * 2:
        return original_string
    
    # Get prefix and suffix of the comparison string
    prefix = comparison_string[:end_length]
    suffix = comparison_string[-end_length:]
    
    result = ""
    i = 0
    
    while i <= len(original_string) - end_length:
        # Check if current position matches the prefix
        if original_string[i:i+end_length] == prefix:
            # Search for the nearest suffix after this position
            for j in range(i + end_length, len(original_string) - end_length + 1):
                if original_string[j:j+end_length] == suffix:
                    # Replace the substring from i to j+end_length
                    result += replacement
                    i = j + end_length  # Move past the replaced substring
                    break
            else:
                # No matching suffix found, keep the original character
                result += original_string[i]
                i += 1
        else:
            # No prefix match, keep the original character
            result += original_string[i]
            i += 1
        
    
    # Add any remaining characters
    result += original_string[i:]
    
    return result


# Example usage:
if __name__ == "__main__":
    # Sample text with PII
    sample_text = """
    Hello, my name is John Smith. You can reach me at john.smith@example.com or 
    call me at (555) 123-4567. My social security number is 123-45-6789 and I live at 
    123 Main St, Anytown, CA 12345.
    """
    
    # Dictionary of identified PII with atomic values (typical from a Pydantic model)
    pii_dictionary = {
        "NAME": "John Smith",
        "EMAIL": "john.smith@example.com",
        "PHONE": "(555) 123-4567",
        "SSN": "123-45-6789",
        "ADDRESS": "123 Main St, Anytown, CA 12345"
    }
    
    # Mask with default format
    masked_text = mask_pii(sample_text, pii_dictionary)
    print("Default masking:")
    print(masked_text)
    
    # Mask with custom format
    custom_masked_text = mask_pii(sample_text, pii_dictionary, mask_format="<REDACTED:{pii_type}>")
    print("\nCustom masking:")
    print(custom_masked_text)

    # Sample masked text
    masked_text = """
    Hello, my name is [NAME]. You can reach me at [EMAIL] or 
    call me at [PHONE]. My social security number is [SSN] and I live at 
    [ADDRESS].
    """

    # Unmask with default format
    unmasked_text = unmask_pii(masked_text, pii_dictionary)
    print("Original text restored:")
    print(unmasked_text)
    
    # Example with custom mask format
    custom_masked_text = """
    Hello, my name is <REDACTED:NAME>. You can reach me at <REDACTED:EMAIL> or 
    call me at <REDACTED:PHONE>. My social security number is <REDACTED:SSN> and I live at 
    <REDACTED:ADDRESS>.
    """
    
    custom_unmasked_text = unmask_pii(custom_masked_text, pii_dictionary, mask_format="<REDACTED:{pii_type}>")
    print("\nOriginal text restored from custom masked format:")
    print(custom_unmasked_text)


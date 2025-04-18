"""
LLM Data Mask - A utility for masking PII in text using LLMs
"""

# Import and expose main functions from core.py
from .core import (
    DriverDetails,
    extract_driver_details,
    process_driver_text,
    check_mapping
)

# Import and expose masking functions from helpers.py
from .helpers import (
    mask_pii,
    unmask_pii,
    remove_extra_spaces_regex,
    fix_comma_spacing_regex,
    replace_if_matches_ends,
)

# Define the public API
__all__ = [
    'DriverDetails',
    'extract_driver_details',
    'process_driver_text',
    'mask_pii',
    'unmask_pii',
    'check_mapping',
    'remove_extra_spaces_regex',
    'fix_comma_spacing_regex',
    'replace_if_matches_ends',
]

# Package metadata
__version__ = '0.1.0'
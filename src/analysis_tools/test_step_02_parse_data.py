#!/usr/bin/env python3
"""
Analysis and testing script for step_02_parse_data.py.
Verifies the functionality of parsing Unicode data.
"""

import os
import random
from src.step_02_parse_data import UnicodeChar, get_parsed_unicode_chars
from src.step_01_download_data import download_unicode_data
from src.config import UNICODE_VERSION

def test_get_parsed_unicode_chars():
    """
    Tests the get_parsed_unicode_chars function to ensure it correctly parses
    the Unicode data and returns a dictionary of UnicodeChar objects.
    """
    print("\n--- Testing get_parsed_unicode_chars function ---")
    
    # Ensure the data file exists
    download_unicode_data(UNICODE_VERSION)
    
    # Get parsed characters
    parsed_chars = get_parsed_unicode_chars(f"UnicodeData-{UNICODE_VERSION}.txt", UNICODE_VERSION)
    
    # Assertions
    assert isinstance(parsed_chars, dict), "Parsed characters should be a dictionary"
    assert len(parsed_chars) > 0, "Parsed characters dictionary should not be empty"
    
    # Test a few known characters
    # 'A' (U+0041)
    char_A = parsed_chars.get(0x0041)
    assert char_A is not None, "Character U+0041 (A) not found"
    assert char_A.name == "LATIN CAPITAL LETTER A", f"Expected name 'LATIN CAPITAL LETTER A', got '{char_A.name}'"
    assert char_A.category == "Lu", f"Expected category 'Lu', got '{char_A.category}'"
    
    # 'é' (U+00E9)
    char_e_acute = parsed_chars.get(0x00E9)
    assert char_e_acute is not None, "Character U+00E9 (é) not found"
    assert char_e_acute.name == "LATIN SMALL LETTER E WITH ACUTE", f"Expected name 'LATIN SMALL LETTER E WITH ACUTE', got '{char_e_acute.name}'"
    assert char_e_acute.category == "Ll", f"Expected category 'Ll', got '{char_e_acute.category}'"

    # '€' (U+20AC)
    char_euro = parsed_chars.get(0x20AC)
    assert char_euro is not None, "Character U+20AC (€) not found"
    assert char_euro.name == "EURO SIGN", f"Expected name 'EURO SIGN', got '{char_euro.name}'"
    assert char_euro.category == "Sc", f"Expected category 'Sc', got '{char_euro.category}'"

    # Test a character that should NOT be in our filtered set (e.g., a CJK character)
    # This assumes our Rust parser filters based on the allowed ranges.
    char_cjk = parsed_chars.get(0x4E00) # A common CJK Unified Ideograph
    assert char_cjk is None, "Character U+4E00 (CJK) should not be found in filtered set"

    print(f"✓ Successfully parsed {len(parsed_chars)} characters.")
    print(f"  Code point range: U+{min(parsed_chars.keys()):04X} - U+{max(parsed_chars.keys()):04X}")
    print("--- parse_unicode_data function tests passed! ---")

if __name__ == "__main__":
    test_parse_data()

#!/usr/bin/env python3
"""
Analysis and testing script for step_02_parse_data.py.
Verifies the functionality of parsing Unicode data.
"""

import os
import random
from src.step_02_parse_data import parse_unicode_data, UnicodeChar
from src.step_01_download_data import download_unicode_data
from src.config import UNICODE_VERSION

def test_parse_data():
    """
    Tests the parse_unicode_data function.
    """
    print("\n" + "=" * 50)
    print("TESTING STEP 02: PARSE UNICODE DATA")
    print("=" * 50)

    filename = f"UnicodeData-{UNICODE_VERSION}.txt"
    
    # Ensure the data file exists
    try:
        download_unicode_data(UNICODE_VERSION)
    except Exception as e:
        print(f"Error ensuring data file exists: {e}")
        print("Skipping parse data test.")
        return

    print(f"Attempting to parse {filename}...")
    try:
        chars_dict = parse_unicode_data(filename)
        
        print(f"\n✓ Successfully parsed {len(chars_dict)} characters.")
        
        if chars_dict:
            # Print summary statistics
            min_cp = min(chars_dict.keys())
            max_cp = max(chars_dict.keys())
            print(f"  Code point range: U+{min_cp:04X} - U+{max_cp:04X}")
            
            # Show a few random characters
            print("\nSample of 5 random parsed characters:")
            sample_cps = random.sample(list(chars_dict.keys()), min(5, len(chars_dict)))
            for cp in sample_cps:
                char_data = chars_dict[cp]
                print(f"  U+{char_data.code_point:04X} ('{chr(char_data.code_point)}'):")
                print(f"    Name: {char_data.name}")
                print(f"    Category: {char_data.category}")
                print(f"    Combining: {char_data.combining}")
                print(f"    Decomposition: {char_data.decomposition if char_data.decomposition else 'N/A'}")
                print(f"    Numeric: {char_data.numeric if char_data.numeric else 'N/A'}")
        else:
            print("  No characters were parsed. Check ALLOWED_RANGES or input file.")

        print("\n" + "=" * 50)
        print("STEP 02 TEST COMPLETED SUCCESSFULLY!")
        print("=" * 50)
            
    except Exception as e:
        print(f"✗ An error occurred during parsing: {e}")
        print("\n" + "=" * 50)
        print("STEP 02 TEST FAILED!")
        print("=" * 50)

if __name__ == "__main__":
    test_parse_data()

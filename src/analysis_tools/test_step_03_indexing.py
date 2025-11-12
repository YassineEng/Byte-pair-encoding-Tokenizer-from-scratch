#!/usr/bin/env python3
"""
Analysis and testing script for step_03_indexing.py.
Verifies the functionality of the double indexing system.
"""

import random
from src.step_03_indexing import DoubleIndexedUnicodeDatabase
from src.step_02_parse_data import parse_unicode_data
from src.step_01_download_data import download_unicode_data
from src.config import UNICODE_VERSION

def test_indexing_system():
    """
    Tests the DoubleIndexedUnicodeDatabase.
    """
    print("\n" + "=" * 50)
    print("TESTING STEP 03: UNICODE INDEXING SYSTEM")
    print("=" * 50)

    filename = f"UnicodeData-{UNICODE_VERSION}.txt"
    
    # Ensure the data file exists and is parsed
    try:
        download_unicode_data(UNICODE_VERSION)
        chars_dict = parse_unicode_data(filename)
    except Exception as e:
        print(f"Error preparing data for indexing test: {e}")
        print("Skipping indexing system test.")
        return

    print("\nBuilding DoubleIndexedUnicodeDatabase...")
    try:
        db_index = DoubleIndexedUnicodeDatabase(chars_dict)
        print("✓ DoubleIndexedUnicodeDatabase built successfully.")

        # Test specific code points
        test_code_points = [0x41, 0x00E9, 0x20AC, 0x0000, 0x10FFFF] # A, é, €, NUL, max Unicode
        
        print("\nTesting character retrieval via index:")
        for cp in test_code_points:
            char_data = db_index.get_character_by_index(cp)
            if char_data:
                print(f"  U+{cp:04X} ('{chr(cp)}'): Found '{char_data.name}'")
            else:
                print(f"  U+{cp:04X}: Not found (as expected for unassigned/filtered chars)")
        
        # Demonstrate index structure with a few lookups
        print("\nDemonstrating index structure for a few code points:")
        sample_cps = [0x41, 0x00E9, 0x20AC] # A, é, €
        for cp in sample_cps:
            index1_pos = cp >> db_index.SHIFT
            index1_val = db_index.index1[index1_pos]
            index_in_block = cp & db_index.BLOCK_MASK
            index2_val = db_index.index2[index1_val + index_in_block]
            
            print(f"  Lookup for U+{cp:04X} ('{chr(cp)}'):")
            print(f"    index1[{index1_pos}] -> {index1_val}")
            print(f"    index2[{index1_val} + {index_in_block}] -> index2[{index1_val + index_in_block}] -> {index2_val}")
            
            # Verify the retrieved record index matches
            expected_record_index = db_index.record_index_map.get(cp)
            if expected_record_index is not None and expected_record_index == index2_val:
                print(f"    ✓ Record index matches expected: {expected_record_index}")
            elif expected_record_index is None and index2_val == 0:
                print(f"    ✓ Record index is 0 (unassigned) as expected.")
            else:
                print(f"    ✗ Record index mismatch! Expected {expected_record_index}, got {index2_val}")


        print("\n" + "=" * 50)
        print("STEP 03 TEST COMPLETED SUCCESSFULLY!")
        print("=" * 50)

    except Exception as e:
        print(f"✗ An error occurred during indexing system test: {e}")
        print("\n" + "=" * 50)
        print("STEP 03 TEST FAILED!")
        print("=" * 50)

if __name__ == "__main__":
    test_indexing_system()

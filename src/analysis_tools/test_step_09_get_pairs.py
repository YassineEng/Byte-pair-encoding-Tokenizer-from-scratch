#!/usr/bin/env python3
"""
Analysis and testing script for step_09_get_pairs.py.
Verifies the functionality of extracting byte pairs.
"""

from src.step_09_get_pairs import get_byte_pairs
from typing import List, Tuple, Dict
from collections import defaultdict

def test_get_byte_pairs():
    """
    Tests the get_byte_pairs function.
    """
    print("\n" + "=" * 50)
    print("TESTING STEP 09: GET BYTE PAIRS")
    print("=" * 50)

    test_cases = [
        ([1, 2, 3, 1, 2], {(1, 2): 2, (2, 3): 1, (3, 1): 1}),
        ([1, 1, 1, 1], {(1, 1): 3}),
        ([1, 2], {(1, 2): 1}),
        ([1], {}),
        ([], {}),
    ]

    all_tests_passed = True
    for tokens, expected_pairs in test_cases:
        print(f"\n--- Testing with tokens: {tokens} ---")
        try:
            actual_pairs = get_byte_pairs(tokens)
            print(f"  Expected pairs: {dict(expected_pairs)}")
            print(f"  Actual pairs:   {dict(actual_pairs)}")
            
            if actual_pairs == expected_pairs:
                print("  ✓ Test Passed")
            else:
                print("  ✗ Test Failed")
                all_tests_passed = False
        except Exception as e:
            print(f"  ✗ An error occurred during test: {e}")
            all_tests_passed = False

    if all_tests_passed:
        print("\n" + "=" * 50)
        print("STEP 09 TEST COMPLETED SUCCESSFULLY!")
        print("=" * 50)
    else:
        print("\n" + "=" * 50)
        print("STEP 09 TEST FAILED! Some assertions did not pass.")
        print("=" * 50)

if __name__ == "__main__":
    test_get_byte_pairs()

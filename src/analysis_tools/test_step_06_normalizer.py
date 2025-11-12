#!/usr/bin/env python3
"""
Analysis and testing script for step_06_normalizer.py.
Verifies the functionality of Unicode normalization forms.
"""

from src.step_06_normalizer import create_normalizer, UnicodeNormalizer

def test_normalization_functions(normalizer: UnicodeNormalizer): # Modified to accept normalizer
    """
    Tests various normalization functions of the UnicodeNormalizer.
    """
    print("\n" + "=" * 50)
    print("TESTING STEP 06: UNICODE NORMALIZATION FUNCTIONS")
    print("=" * 50)

    # Use the provided normalizer object directly
    # Removed the internal create_normalizer() call

    test_cases = [
        # (input_string, form, expected_output)
        ("café", "NFC", "café"),
        ("cafe\u0301", "NFC", "café"), # e + acute accent -> é
        ("café", "NFD", "cafe\u0301"),
        ("cafe\u0301", "NFD", "cafe\u0301"),
        ("ﬃ", "NFKC", "ffi"), # Compatibility decomposition
        ("ﬃ", "NFKD", "ffi"), # Compatibility decomposition
        ("ﬁ", "NFC", "ﬁ"),
        ("ﬁ", "NFD", "f\u0069"),
        ("U\u0308", "NFC", "Ü"), # U + diaeresis -> Ü
        ("Ü", "NFD", "U\u0308"),
        ("U\u0308", "NFKC", "Ü"),
        ("Ü", "NFKD", "U\u0308"),
        ("Å", "NFC", "Å"), # Angstrom sign -> A with ring above
        ("Å", "NFD", "A\u030a"),
        ("Å", "NFKC", "Å"),
        ("Å", "NFKD", "A\u030a"),
        ("1\u20442", "NFKC", "1/2"), # Fraction slash
        ("1\u20442", "NFKD", "1/2"),
    ]

    all_tests_passed = True
    for input_str, form, expected_output in test_cases:
        print(f"\n--- Testing '{input_str}' with form '{form}' ---")
        try:
            actual_output = normalizer.normalize(input_str, form)
            print(f"  Input: '{input_str}'")
            print(f"  Form: {form}")
            print(f"  Expected: '{expected_output}' (Code Points: {[f'U+{ord(c):04X}' for c in expected_output]})")
            print(f"  Actual:   '{actual_output}' (Code Points: {[f'U+{ord(c):04X}' for c in actual_output]})")
            
            if actual_output == expected_output:
                print("  ✓ Test Passed")
            else:
                print("  ✗ Test Failed")
                all_tests_passed = False
        except Exception as e:
            print(f"  ✗ An error occurred during test: {e}")
            all_tests_passed = False

    if all_tests_passed:
        print("\n" + "=" * 50)
        print("STEP 06 TEST COMPLETED SUCCESSFULLY!")
        print("=" * 50)
    else:
        print("\n" + "=" * 50)
        print("STEP 06 TEST FAILED! Some assertions did not pass.")
        print("=" * 50)

if __name__ == "__main__":
    # For standalone execution, create the normalizer
    print("\nCreating normalizer for standalone normalization tests...")
    normalizer = create_normalizer()
    test_normalization_functions(normalizer)
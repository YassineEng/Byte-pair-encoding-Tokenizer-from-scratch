#!/usr/bin/env python3
"""
Analysis and testing script for step_05_lookup.py.
Verifies the functionality of Unicode character lookup functions.
"""

from src.step_04_database_builder import build_database
from src.step_05_lookup import UnicodeDatabaseWithIndex

def test_lookup_functions():
    """
    Tests various lookup functions of the UnicodeDatabaseWithIndex.
    """
    print("\n" + "=" * 50)
    print("TESTING STEP 05: UNICODE LOOKUP FUNCTIONS")
    print("=" * 50)

    try:
        database = build_database()
        print("✓ Unicode database initialized for lookup tests.")
    except Exception as e:
        print(f"Error initializing database for lookup tests: {e}")
        print("Skipping lookup functions test.")
        return

    test_chars_and_props = [
        ('A', {'name': 'LATIN CAPITAL LETTER A', 'category': 'Lu', 'decimal': None, 'digit': None, 'numeric': None, 'combining': 0, 'bidirectional': 'L', 'mirrored': 0, 'decomposition': ''}),
        ('é', {'name': 'LATIN SMALL LETTER E WITH ACUTE', 'category': 'Ll', 'decimal': None, 'digit': None, 'numeric': None, 'combining': 0, 'bidirectional': 'L', 'mirrored': 0, 'decomposition': '0065 0301'}),
        ('€', {'name': 'EURO SIGN', 'category': 'Sc', 'decimal': None, 'digit': None, 'numeric': None, 'combining': 0, 'bidirectional': 'ET', 'mirrored': 0, 'decomposition': ''}),
        ('9', {'name': 'DIGIT NINE', 'category': 'Nd', 'decimal': 9, 'digit': 9, 'numeric': 9.0, 'combining': 0, 'bidirectional': 'L', 'mirrored': 0, 'decomposition': ''}),
        ('½', {'name': 'VULGAR FRACTION ONE HALF', 'category': 'No', 'decimal': None, 'digit': None, 'numeric': 0.5, 'combining': 0, 'bidirectional': 'L', 'mirrored': 0, 'decomposition': '<compat> 0031 2044 0032'}),
        (' ', {'name': 'SPACE', 'category': 'Zs', 'decimal': None, 'digit': None, 'numeric': None, 'combining': 0, 'bidirectional': 'WS', 'mirrored': 0, 'decomposition': ''}),
    ]

    all_tests_passed = True
    for char_str, expected_props in test_chars_and_props:
        print(f"\n--- Testing '{char_str}' (U+{ord(char_str):04X}) ---")
        cp = ord(char_str)
        
        try:
            # Test name()
            actual_name = database.name(char_str, default="N/A")
            print(f"  Name: Expected='{expected_props['name']}', Actual='{actual_name}' {'✓' if actual_name == expected_props['name'] else '✗'}")
            if actual_name != expected_props['name']: all_tests_passed = False

            # Test category()
            actual_category = database.category(char_str)
            print(f"  Category: Expected='{expected_props['category']}', Actual='{actual_category}' {'✓' if actual_category == expected_props['category'] else '✗'}")
            if actual_category != expected_props['category']: all_tests_passed = False

            # Test decimal()
            actual_decimal = database.decimal(char_str, default=None)
            print(f"  Decimal: Expected='{expected_props['decimal']}', Actual='{actual_decimal}' {'✓' if actual_decimal == expected_props['decimal'] else '✗'}")
            if actual_decimal != expected_props['decimal']: all_tests_passed = False

            # Test digit()
            actual_digit = database.digit(char_str, default=None)
            print(f"  Digit: Expected='{expected_props['digit']}', Actual='{actual_digit}' {'✓' if actual_digit == expected_props['digit'] else '✗'}")
            if actual_digit != expected_props['digit']: all_tests_passed = False

            # Test numeric()
            actual_numeric = database.numeric(char_str, default=None)
            print(f"  Numeric: Expected='{expected_props['numeric']}', Actual='{actual_numeric}' {'✓' if actual_numeric == expected_props['numeric'] else '✗'}")
            if actual_numeric != expected_props['numeric']: all_tests_passed = False

            # Test combining()
            actual_combining = database.combining(char_str)
            print(f"  Combining: Expected='{expected_props['combining']}', Actual='{actual_combining}' {'✓' if actual_combining == expected_props['combining'] else '✗'}")
            if actual_combining != expected_props['combining']: all_tests_passed = False

            # Test bidirectional()
            actual_bidirectional = database.bidirectional(char_str)
            print(f"  Bidi: Expected='{expected_props['bidirectional']}', Actual='{actual_bidirectional}' {'✓' if actual_bidirectional == expected_props['bidirectional'] else '✗'}")
            if actual_bidirectional != expected_props['bidirectional']: all_tests_passed = False

            # Test mirrored()
            actual_mirrored = database.mirrored(char_str)
            print(f"  Mirrored: Expected='{expected_props['mirrored']}', Actual='{actual_mirrored}' {'✓' if actual_mirrored == expected_props['mirrored'] else '✗'}")
            if actual_mirrored != expected_props['mirrored']: all_tests_passed = False

            # Test decomposition()
            actual_decomposition = database.decomposition(char_str)
            print(f"  Decomp: Expected='{expected_props['decomposition']}', Actual='{actual_decomposition}' {'✓' if actual_decomposition == expected_props['decomposition'] else '✗'}")
            if actual_decomposition != expected_props['decomposition']: all_tests_passed = False

        except Exception as e:
            print(f"  ✗ An error occurred during test for '{char_str}': {e}")
            all_tests_passed = False

    if all_tests_passed:
        print("\n" + "=" * 50)
        print("STEP 05 TEST COMPLETED SUCCESSFULLY!")
        print("=" * 50)
    else:
        print("\n" + "=" * 50)
        print("STEP 05 TEST FAILED! Some assertions did not pass.")
        print("=" * 50)

if __name__ == "__main__":
    test_lookup_functions()

#!/usr/bin/env python3
"""
Analysis and testing script for the custom UTF-8 encoder/decoder (Step 07).
"""

from typing import List, Tuple, Dict

# Import from our custom modules
from src.step_07_utf8_codec import CustomUTF8Codec

def demonstrate_custom_utf8():
    """
    Test our custom UTF-8 encoder/decoder.
    NOTE: The test cases are limited to characters within the ALLOWED_RANGES
    defined in parse_data.py (e.g., Basic Latin, Latin-1 Supplement) to
    reflect the current simplified scope of the project.
    """
    print("CUSTOM UTF-8 ENCODER/DECODER TEST")
    print("=" * 50)
    
    test_cases = [
        "A",           # Basic ASCII (1 byte)
        "é",           # Latin-1 (2 bytes)
        "€",           # A 3-byte character from the Currency Symbols block
        "Hello, world!", # Mixed ASCII
        "café résumé", # Mixed Latin-1
    ]
    
    for text in test_cases:
        print(f"\nText: '{text}'")
        
        # Our custom encoding
        custom_bytes = CustomUTF8Codec.encode(text)
        custom_decoded = CustomUTF8Codec.decode(custom_bytes)
        
        # Python's built-in encoding (for comparison)
        python_bytes = list(text.encode('utf-8'))
        python_decoded = bytes(python_bytes).decode('utf-8')
        
        print(f"  Code points: {[f'U+{ord(c):04X}' for c in text]}")
        print(f"  Custom bytes: {custom_bytes}")
        print(f"  Python bytes: {python_bytes}")
        print(f"  Bytes match: {custom_bytes == python_bytes}")
        print(f"  Custom decoded: '{custom_decoded}'")
        print(f"  Round-trip works: {custom_decoded == text}")

def compare_with_python_builtin():
    """Compare our implementation with Python's built-in functions"""
    print("\n" + "=" * 50)
    print("COMPARISON WITH PYTHON BUILT-IN")
    print("=" * 50)
    
    test_strings = ["A", "é", "€", "café", "Hello, world!"]
    
    for text in test_strings:
        print(f"\n'{text}':")
        
        # Our implementation
        our_bytes = CustomUTF8Codec.encode(text)
        our_decoded = CustomUTF8Codec.decode(our_bytes)
        
        # Python's implementation  
        python_bytes = list(text.encode('utf-8'))
        python_decoded = bytes(python_bytes).decode('utf-8')
        
        print(f"  Our bytes:    {our_bytes}")
        print(f"  Python bytes: {python_bytes}")
        print(f"  Match: {our_bytes == python_bytes}")
        print(f"  Our decode: '{our_decoded}'")
        print(f"  Python decode: '{python_decoded}'")
        print(f"  Both work: {our_decoded == python_decoded == text}")

if __name__ == "__main__":
    demonstrate_custom_utf8()
    compare_with_python_builtin()

# NOTE: This project is simplified for educational purposes and only processes
# a subset of Unicode characters defined in ALLOWED_RANGES. This keeps the
# database small and the parsing fast. To process all of Unicode, the
# ALLOWED_RANGES filter and the is_allowed_code_point function can be removed.
from collections import namedtuple
from typing import Dict
import sys

from src.text_encoding.step_06_utf8_codec import CustomUTF8Codec

# Define the character data structure
UnicodeChar = namedtuple('UnicodeChar', [
    'code_point',      # int: Unicode code point (e.g., 0x00C0)
    'name',            # str: Character name
    'category',        # str: General category (e.g., 'Lu', 'Nd')
    'combining',       # int: Canonical combining class (0-255)
    'bidirectional',   # str: Bidirectional class (e.g., 'L', 'R')
    'decomposition',   # str: Decomposition mapping
    'decimal',         # Optional[int]: Decimal digit value
    'digit',           # Optional[int]: Digit value  
    'numeric',         # Optional[str]: Numeric value (as string)
    'mirrored',        # str: 'Y' or 'N' for bidirectional mirroring
    'unicode1_name',   # str: Unicode 1.0 name
    'iso_comment',     # str: ISO 10646 comment
    'uppercase',       # Optional[int]: Uppercase mapping
    'lowercase',       # Optional[int]: Lowercase mapping
    'titlecase',       # Optional[int]: Titlecase mapping
])

def parse_unicode_data(filename: str) -> Dict[int, UnicodeChar]:
    """
    Parse the UnicodeData.txt file and return a dictionary mapping
    code points to UnicodeChar objects, filtered for English, numbers, punctuation.
    Uses CustomUTF8Codec for decoding.
    """
    chars = {}
    line_count = 0
    assigned_chars = 0
    
    # Define the allowed code point ranges for simplification
    # Basic Latin (ASCII)
    # Latin-1 Supplement (common accented chars)
    # General Punctuation
    # Currency Symbols
    # Mathematical Operators
    ALLOWED_RANGES = [
        range(0x0000, 0x007F + 1),  # Basic Latin (ASCII)
        range(0x0080, 0x00FF + 1),  # Latin-1 Supplement
        range(0x2000, 0x206F + 1),  # General Punctuation
        range(0x20A0, 0x20CF + 1),  # Currency Symbols
        range(0x2200, 0x22FF + 1),  # Mathematical Operators
    ]

    def is_allowed_code_point(code_point: int) -> bool:
        for r in ALLOWED_RANGES:
            if code_point in r:
                return True
        return False

    print(f"Parsing {filename} and filtering for English, numbers, punctuation using CustomUTF8Codec...")
    
    try:
        with open(filename, 'rb') as f: # Open in binary mode
            byte_content = f.read()
            # Convert bytes to a list of integers (byte values)
            byte_list = list(byte_content)
            
            # Decode using CustomUTF8Codec
            decoded_content = CustomUTF8Codec.decode(byte_list)
            
            for line_num, line in enumerate(decoded_content.splitlines(), 1):
                line = line.strip()
                line_count += 1
                
                # Skip empty lines and comments
                if not line or line.startswith('#'):
                    continue
                
                # Split into fields (should be exactly 15 fields)
                fields = line.split(';')
                if len(fields) != 15:
                    # print(f"Warning: Line {line_num} has {len(fields)} fields (expected 15): {line}")
                    continue
                
                # Parse code point (field 0)
                try:
                    code_point = int(fields[0], 16)
                except ValueError as e:
                    print(f"Error parsing code point on line {line_num}: {fields[0]}")
                    continue
                
                # Filter characters based on allowed ranges
                if not is_allowed_code_point(code_point):
                    continue

                # Parse numeric fields (with proper handling of empty values)
                try:
                    combining = int(fields[3]) if fields[3] else 0
                except ValueError:
                    combining = 0
                
                # Parse decimal, digit, numeric (fields 6, 7, 8)
                decimal = int(fields[6]) if fields[6] else None
                digit = int(fields[7]) if fields[7] else None
                numeric = fields[8] if fields[8] else None
                
                # Parse case mappings (fields 12, 13, 14)
                uppercase = int(fields[12], 16) if fields[12] else None
                lowercase = int(fields[13], 16) if fields[13] else None
                titlecase = int(fields[14], 16) if fields[14] else None
                
                # Create UnicodeChar object
                char = UnicodeChar(
                    code_point=code_point,
                    name=fields[1],
                    category=fields[2],
                    combining=combining,
                    bidirectional=fields[4],
                    decomposition=fields[5],
                    decimal=decimal,
                    digit=digit,
                    numeric=numeric,
                    mirrored=fields[9],
                    unicode1_name=fields[10],
                    iso_comment=fields[11],
                    uppercase=uppercase,
                    lowercase=lowercase,
                    titlecase=titlecase,
                )
                
                chars[code_point] = char
                assigned_chars += 1
                
                # Progress reporting for large files
                if assigned_chars % 100 == 0: # Reduced frequency for smaller dataset
                    print(f"  Processed {assigned_chars} filtered characters...")
                    
    except FileNotFoundError:
        print(f"Error: File {filename} not found!")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file {filename}: {e}")
        sys.exit(1)
    
    print(f"Parsing complete:")
    print(f"  Total lines processed: {line_count}")
    print(f"  Assigned filtered characters: {assigned_chars}")
    if chars:
        print(f"  Code point range: 0x{min(chars.keys()):04X} - 0x{max(chars.keys()):04X}")
    else:
        print("  No characters found within the specified ranges.")
    
    return chars
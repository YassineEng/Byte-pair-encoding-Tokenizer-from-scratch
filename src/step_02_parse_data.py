# NOTE: This project is simplified for educational purposes and only processes
# a subset of Unicode characters defined in ALLOWED_RANGES. This keeps the
# database small and the parsing fast. To process all of Unicode, the
# ALLOWED_RANGES filter and the is_allowed_code_point function can be removed.
from collections import namedtuple
from typing import Dict
import sys
import pickle
import os
import rust_parser

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

PARSED_CHARS_CACHE_FILENAME = "outputs/parsed_chars.bin"

def get_parsed_unicode_chars(filename: str, version: str) -> Dict[int, UnicodeChar]:
    """
    Loads parsed Unicode characters from cache if available and up-to-date,
    otherwise parses the data and caches the result.
    """
    if os.path.exists(PARSED_CHARS_CACHE_FILENAME):
        try:
            with open(PARSED_CHARS_CACHE_FILENAME, "rb") as f:
                cached_data = pickle.load(f)
                if cached_data.get('version') == version:
                    print(f"Loading parsed Unicode characters from cache: {PARSED_CHARS_CACHE_FILENAME}")
                    return cached_data['chars']
                else:
                    print(f"Parsed characters cache is for version {cached_data.get('version', 'N/A')}, but version {version} is required. Re-parsing...")
        except (EOFError, AttributeError, pickle.UnpicklingError, KeyError) as e:
            print(f"Error loading parsed characters cache ({e}). Re-parsing...")
    else:
        print("Parsed characters cache file not found. Re-parsing...")

    # If cache fails or not found, parse from scratch
    # Note: We are now calling the Rust-based parser
    print(f"Parsing {filename} and filtering for English, numbers, punctuation using Rust parser...")
    chars = rust_parser.parse_unicode_data(filename)
    
    # Save the new parsed characters to the cache
    try:
        os.makedirs(os.path.dirname(PARSED_CHARS_CACHE_FILENAME), exist_ok=True)
        with open(PARSED_CHARS_CACHE_FILENAME, "wb") as f:
            print(f"Caching parsed Unicode characters to: {PARSED_CHARS_CACHE_FILENAME}")
            pickle.dump({'version': version, 'chars': chars}, f)
    except Exception as e:
        print(f"Error: Could not write parsed characters to cache file: {e}")
            
    return chars

#!/usr/bin/env python3
"""
Standalone script to visualize the contents of the cached Unicode database.
"""

import pickle
import random
from src.step_05_lookup import UnicodeDatabaseWithIndex
from src.step_02_parse_data import UnicodeChar

CACHE_FILENAME = "unicode_database.bin"

def visualize_database(database: UnicodeDatabaseWithIndex):
    """Prints a human-readable visualization of the database contents."""
    
    print("="*60)
    print("UNICODE DATABASE VISUALIZATION")
    print("="*60)

    # 1. Summary Statistics
    print("\n--- 1. Summary Statistics ---")
    print(f"Unicode Version: {getattr(database, 'version', 'N/A')}")
    print(f"Total Characters in DB: {len(database.chars)}")
    print(f"Index 1 Size (Blocks): {len(database.index1)}")
    print(f"Index 2 Size (Pointers): {len(database.index2)}")

    # 2. Index Visualization
    print("\n--- 2. Indexing System ---")
    print("The database uses a two-level index to find character data quickly.")
    print("  - index1 maps a code point block to a position in index2.")
    print("  - index2 contains the actual pointers to the character records.")
    
    # Show a few entries from index1
    print("\nSample of index1 (first 10 entries):")
    print(database.index1[:10])
    
    # Explain and show a sample from index2
    print("\nSample of index2 (first 32 entries):")
    print(database.index2[:32])
    
    # Demonstrate a lookup
    sample_cp = 0x41 # 'A'
    print(f"\nExample Lookup for U+{sample_cp:04X} ('A'):")
    index1_pos = sample_cp >> 8
    index1_val = database.index1[index1_pos]
    print(f"  1. Go to index1[{index1_pos}] -> Value is {index1_val}")
    
    index2_pos = index1_val + (sample_cp & 0xFF)
    index2_val = database.index2[index2_pos]
    print(f"  2. Go to index2[{index1_val} + {sample_cp & 0xFF}] -> index2[{index2_pos}] -> Value is {index2_val}")
    
    char_record = database.records[index2_val]
    print(f"  3. Go to records[{index2_val}] -> Found character: '{char_record.name}'")

    # 3. Character Record Samples
    print("\n--- 3. Character Record Samples ---")
    print("Here are a few random character records from the database:")
    
    if not database.chars:
        print("No characters in the database to sample.")
        return

    # Get a few random code points from the database
    random_code_points = random.sample(list(database.chars.keys()), min(5, len(database.chars)))
    
    for cp in random_code_points:
        char_data = database.chars[cp]
        print(f"\n--- Character: '{chr(cp)}' (U+{cp:04X}) ---")
        print(f"  Name:      {char_data.name}")
        print(f"  Category:  {char_data.category}")
        print(f"  Combining: {char_data.combining}")
        print(f"  Bidi Class:{char_data.bidirectional}")
        print(f"  Decomp:    {char_data.decomposition if char_data.decomposition else 'N/A'}")
        print(f"  Numeric:   {char_data.numeric if char_data.numeric else 'N/A'}")
        print(f"  Mirrored:  {char_data.mirrored}")

    print("\n" + "="*60)

if __name__ == "__main__":
    try:
        with open(CACHE_FILENAME, "rb") as f:
            print(f"Loading Unicode database from cache: {CACHE_FILENAME}")
            db = pickle.load(f)
            visualize_database(db)
    except FileNotFoundError:
        print(f"Error: Cache file '{CACHE_FILENAME}' not found.")
        print("Please run `python -m src.main` first to build the database.")
    except Exception as e:
        print(f"An error occurred: {e}")

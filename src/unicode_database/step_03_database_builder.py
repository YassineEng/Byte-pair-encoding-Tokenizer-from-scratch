#!/usr/bin/env python3
"""
Step 2.5: Build Double Indexing System
Replicating Python's efficient Unicode character lookup
"""

import sys
import pickle
import os # Import os for path checking
from typing import Dict, List, Tuple

# Import from our previous steps
from src.config import UNICODE_VERSION
from src.data_preparation.step_01_download_data import download_unicode_data
from src.data_preparation.step_02_parse_data import UnicodeChar, parse_unicode_data
from src.unicode_database.step_04_lookup import UnicodeDatabaseWithIndex

CACHE_FILENAME = "unicode_database.bin"

def build_database():
    """
    Builds the Unicode database, loading from a cache if available,
    otherwise building it from scratch and caching the result.
    """
    # 1. Try to load from cache
    if os.path.exists(CACHE_FILENAME):
        try:
            with open(CACHE_FILENAME, "rb") as f:
                print(f"Loading Unicode database from cache: {CACHE_FILENAME}")
                database = pickle.load(f)
                # Verify that the cached version matches the required version
                if hasattr(database, 'version') and database.version == UNICODE_VERSION:
                    print("✓ Database loaded successfully.")
                    return database
                else:
                    print(f"Cache is for version {getattr(database, 'version', 'N/A')}, but version {UNICODE_VERSION} is required. Rebuilding...")
        except (EOFError, AttributeError, pickle.UnpicklingError) as e:
            print(f"Error loading cache ({e}). Building database from scratch...")
    else:
        print("Cache file not found. Building database from scratch...")

    # 2. If cache fails or not found, build from scratch
    print("="*60)
    print("STEP 2.5: IMPLEMENT DOUBLE INDEXING SYSTEM")
    print("Replicating Python's efficient Unicode lookup")
    print("="*60)
    
    try:
        filename = download_unicode_data(UNICODE_VERSION)
        chars = parse_unicode_data(filename)
    except Exception as e:
        print(f"Error: Could not load data from Step 1: {e}")
        sys.exit(1)
    
    print("\nBuilding double-indexed Unicode database...")
    database = UnicodeDatabaseWithIndex(chars)
    database.version = UNICODE_VERSION  # Stamp the database with the version
    
    # 3. Save the new database to the cache
    try:
        with open(CACHE_FILENAME, "wb") as f:
            print(f"Caching new database to: {CACHE_FILENAME}")
            pickle.dump(database, f)
    except Exception as e:
        print(f"Error: Could not write to cache file: {e}")

    # Verification step
    print("\n" + "="*50)
    print("VERIFYING UNICODE FUNCTIONS STILL WORK")
    print("="*50)
    
    test_chars = ['A', '9', 'À']
    for char in test_chars:
        print(f"\n'{char}':")
        print(f"  Name: {database.name(char)}")
        print(f"  Category: {database.category(char)}")
        print(f"  Decimal: {database.decimal(char, 'N/A')}")
    
    print("\n" + "="*60)
    print("STEP 2.5 COMPLETED SUCCESSFULLY!")
    print("✓ Implemented double indexing system")
    print("✓ Replicated Python's efficient lookup")
    print("✓ Ready for normalization functions!")
    print("="*60)
    
    return database

if __name__ == "__main__":
    database = build_database()
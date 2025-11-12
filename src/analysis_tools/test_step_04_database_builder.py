#!/usr/bin/env python3
"""
Analysis and testing script for step_04_database_builder.py.
Verifies the functionality of building and caching the Unicode database.
"""

import os
import pickle
from src.step_04_database_builder import build_database, CACHE_FILENAME
from src.step_05_lookup import UnicodeDatabaseWithIndex
from src.config import UNICODE_VERSION

def test_database_builder():
    """
    Tests the build_database function, including caching.
    """
    print("\n" + "=" * 50)
    print("TESTING STEP 04: UNICODE DATABASE BUILDER")
    print("=" * 50)

    # Clean up previous cache if it exists
    if os.path.exists(CACHE_FILENAME):
        print(f"Removing existing cache file: {CACHE_FILENAME}")
        os.remove(CACHE_FILENAME)

    print("\n--- First build (should build from scratch) ---")
    try:
        db1 = build_database()
        print("✓ First database build successful.")
        assert os.path.exists(CACHE_FILENAME), "Cache file was not created."
        assert isinstance(db1, UnicodeDatabaseWithIndex), "Returned object is not UnicodeDatabaseWithIndex."
        assert hasattr(db1, 'version') and db1.version == UNICODE_VERSION, "Database version mismatch."
        print(f"  Database version: {db1.version}")
        print(f"  Total characters: {len(db1.chars)}")
        
        # Verify some basic lookups
        print("\nVerifying basic lookups on first build:")
        test_chars = ['A', '9', 'À']
        for char in test_chars:
            name = db1.name(char, default="N/A")
            category = db1.category(char)
            print(f"  '{char}': Name='{name}', Category='{category}'")
            assert name != "N/A", f"Lookup for '{char}' failed."

    except Exception as e:
        print(f"✗ Error during first database build: {e}")
        print("\n" + "=" * 50)
        print("STEP 04 TEST FAILED!")
        print("=" * 50)
        return

    print("\n--- Second build (should load from cache) ---")
    try:
        db2 = build_database()
        print("✓ Second database build successful (should be from cache).")
        assert isinstance(db2, UnicodeDatabaseWithIndex), "Returned object is not UnicodeDatabaseWithIndex."
        assert hasattr(db2, 'version') and db2.version == UNICODE_VERSION, "Database version mismatch."
        print(f"  Database version: {db2.version}")
        print(f"  Total characters: {len(db2.chars)}")
        
        # Verify some basic lookups
        print("\nVerifying basic lookups on second build (from cache):")
        test_chars = ['A', '9', 'À']
        for char in test_chars:
            name = db2.name(char, default="N/A")
            category = db2.category(char)
            print(f"  '{char}': Name='{name}', Category='{category}'")
            assert name != "N/A", f"Lookup for '{char}' failed."

    except Exception as e:
        print(f"✗ Error during second database build (cache load): {e}")
        print("\n" + "=" * 50)
        print("STEP 04 TEST FAILED!")
        print("=" * 50)
        return

    print("\n" + "=" * 50)
    print("STEP 04 TEST COMPLETED SUCCESSFULLY!")
    print("=" * 50)

if __name__ == "__main__":
    test_database_builder()

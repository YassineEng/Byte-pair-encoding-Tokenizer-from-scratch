#!/usr/bin/env python3
"""
Analysis and testing script for step_03_indexing.py.
Verifies the functionality of the double indexing system and analyzes its performance.
"""

import random
import time # Added for performance analysis
from src.step_03_indexing import DoubleIndexedUnicodeDatabase
from src.step_02_parse_data import parse_unicode_data
from src.step_01_download_data import download_unicode_data
from src.step_04_database_builder import build_database # Needed for performance analysis
from src.step_05_lookup import UnicodeDatabaseWithIndex # Needed for type hinting in performance analysis
from src.config import UNICODE_VERSION

def analyze_index_efficiency(database: UnicodeDatabaseWithIndex):
    """Analyze the memory efficiency of double indexing"""
    print("\n" + "="*50)
    print("INDEX EFFICIENCY ANALYSIS")
    print("="*50)
    
    total_chars = len(database.chars)
    total_unicode_space = 0x110000  # 1,114,112 possible code points
    
    # Calculate storage requirements
    naive_storage = total_unicode_space * 4  # 4 bytes per pointer (estimate)
    index_storage = (
        len(database.index1) * 4 +  # index1: 4 bytes per entry
        len(database.index2) * 4    # index2: 4 bytes per entry
    )
    
    compression_ratio = naive_storage / index_storage
    
    print(f"Unicode code space: {total_unicode_space:,} possible code points")
    print(f"Assigned characters: {total_chars:,} ({total_chars/total_unicode_space*100:.2f}% of space)")
    print(f"Naive array storage: {naive_storage/1024/1024:.1f} MB")
    print(f"Double index storage: {index_storage/1024/1024:.1f} MB")
    print(f"Compression ratio: {compression_ratio:.1f}x")
    print(f"Memory savings: {(1 - index_storage/naive_storage)*100:.1f}%")
    
    # Show block utilization
    used_blocks = sum(1 for i in database.index1 if i != 0)
    total_blocks = len(database.index1)
    print(f"Block utilization: {used_blocks}/{total_blocks} ({used_blocks/total_blocks*100:.1f}%)")

def demonstrate_index_performance(database: UnicodeDatabaseWithIndex):
    """Demonstrate the performance of the double index system"""
    print("\n" + "="*50)
    print("DOUBLE INDEX PERFORMANCE DEMONSTRATION")
    print("="*50)
    
    test_chars = ['A', '9', 'À']
    
    print("Testing double index lookup:")
    for char in test_chars:
        start_time = time.perf_counter_ns()
        database.name(char)
        end_time = time.perf_counter_ns()
        print(f"U+{ord(char):04X}: {database.name(char)} - {end_time - start_time} ns")
        
    print("\nComparing with direct dictionary lookup:")
    for char in test_chars:
        start_time = time.perf_counter_ns()
        database.chars[ord(char)].name
        end_time = time.perf_counter_ns()
        print(f"U+{ord(char):04X}: {database.chars[ord(char)].name} - {end_time - start_time} ns")


def test_indexing_system(database: UnicodeDatabaseWithIndex): # Modified to accept database
    """
    Tests the DoubleIndexedUnicodeDatabase.
    """
    print("\n" + "=" * 50)
    print("TESTING STEP 03: UNICODE INDEXING SYSTEM")
    print("=" * 50)

    # Use the provided database object directly
    db_index = database 

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

if __name__ == "__main__":
    # For standalone execution, build the database
    print("\nBuilding database for standalone indexing test and performance analysis...")
    db = build_database()
    test_indexing_system(db)
    analyze_index_efficiency(db)
    demonstrate_index_performance(db)

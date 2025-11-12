#!/usr/bin/env python3
"""
Step 2.5: Build Double Indexing System
Replicating Python's efficient Unicode character lookup
"""

import sys
from typing import Dict, List, Tuple
import array
import time

# Import from our previous steps
from src.config import UNICODE_VERSION
from src.data_preparation.download_data import download_unicode_data
from src.data_preparation.parse_data import UnicodeChar, parse_unicode_data
from src.unicode_database.lookup import UnicodeDatabaseWithIndex

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

def build_database():
    """Main function for Step 2.5"""
    print("="*60)
    print("STEP 2.5: IMPLEMENT DOUBLE INDEXING SYSTEM")
    print("Replicating Python's efficient Unicode lookup")
    print("="*60)
    
    # Get data from Step 1
    try:
        filename = download_unicode_data(UNICODE_VERSION)
        
        # parse_unicode_data no longer needs blocks, scripts, prop_list
        chars = parse_unicode_data(filename)
    except Exception as e:
        print(f"Error: Could not load data from Step 1: {e}")
        sys.exit(1)
    
    # Build database with double indexing
    print("\nBuilding double-indexed Unicode database...")
    database = UnicodeDatabaseWithIndex(chars)
    
    # Analyze efficiency
    analyze_index_efficiency(database)
    
    # Demonstrate performance
    database.demonstrate_index_performance()
    
    # Test that all functions still work
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
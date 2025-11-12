#!/usr/bin/env python3
"""
Standalone script for performance analysis of the Unicode database.
"""

import time
from src.unicode_database.database_builder import build_database
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

if __name__ == "__main__":
    print("Building database for performance analysis...")
    db = build_database()
    analyze_index_efficiency(db)
    demonstrate_index_performance(db)

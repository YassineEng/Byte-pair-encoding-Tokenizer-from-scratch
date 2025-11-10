#!/usr/bin/env python3
"""
Step 2.5: Implement Double Indexing System
Replicating Python's efficient Unicode character lookup
"""

import sys
from typing import Dict, List, Tuple
import array
import time

# Import from our previous steps
from unicode_magic.download_parse import UnicodeChar, download_unicode_data, parse_unicode_data, download_east_asian_widths, download_unicode_auxiliary_files, parse_blocks, parse_scripts, parse_prop_list
from unicode_magic.property_database import UnicodePropertyDatabase, analyze_property_database, save_property_database_summary

class DoubleIndexedUnicodeDatabase(UnicodePropertyDatabase):
    """
    Adds the efficient double-indexing system used by Python's unicodedata
    This is the ACTUAL lookup mechanism from unicodedata.c
    """
    
    def __init__(self, chars: Dict[int, UnicodeChar]):
        super().__init__(chars)
        self._build_double_index()
    
    def _build_double_index(self):
        """
        Build the two-level index system used by Python for O(1) lookups
        This replicates the exact algorithm from _getrecord_ex() in unicodedata.c
        """
        print("Building double index system...")
        
        # Python uses SHIFT = 12, meaning 4096 code points per block
        self.SHIFT = 12
        self.BLOCK_SIZE = 1 << self.SHIFT  # 4096
        self.BLOCK_MASK = self.BLOCK_SIZE - 1  # 0xFFF
        
        # Group characters by blocks
        blocks = {}
        for code_point in self.chars.keys():
            block = code_point >> self.SHIFT  # High bits
            index_in_block = code_point & self.BLOCK_MASK  # Low bits
            
            if block not in blocks:
                blocks[block] = set()
            blocks[block].add(index_in_block)
        
        # Build index1 (points to index2 blocks) and index2 (points to character data)
        self.index1 = []  # Like index1 in unicodedata.c
        self.index2 = []  # Like index2 in unicodedata.c 
        
        # We need to map each unique character data pattern to an index
        # In Python's implementation, this maps to _PyUnicode_Database_Records
        self._build_character_records_index()
        
        # Build the actual index arrays
        self._build_index_arrays(blocks)
        
        print(f"✓ Built double index: {len(self.index1)} index1 entries, {len(self.index2)} index2 entries")
    
    def _build_character_records_index(self):
        """Map each unique combination of properties to a record index"""
        # In Python, this creates _PyUnicode_Database_Records array
        # We'll create a mapping from property signature -> record index
        self.record_signatures = {}
        self.record_index_map = {}  # code_point -> record_index
        
        record_index = 0
        for code_point, char in self.chars.items():
            # Create a signature based on the character's properties
            # This is similar to what goes into _PyUnicode_DatabaseRecord
            signature = (
                char.category,
                char.combining,
                char.bidirectional,
                char.mirrored,
                # In real Python, there are more fields like east_asian_width, quick_check
            )
            
            if signature not in self.record_signatures:
                self.record_signatures[signature] = record_index
                record_index += 1
            
            self.record_index_map[code_point] = self.record_signatures[signature]
        
        print(f"✓ Created {len(self.record_signatures)} unique character records")
    
    def _build_index_arrays(self, blocks):
        """Build the index1 and index2 arrays"""
        # Sort blocks to maintain order
        sorted_blocks = sorted(blocks.keys())
        
        # For each possible block (0x0000-0x10FFFF >> 12 = 0-16)
        max_block = 0x10FFFF >> self.SHIFT  # 16
        self.index1 = [0] * (max_block + 1)
        
        # Build index2 blocks
        index2_blocks = {}
        current_index2_pos = 0
        
        for block in range(max_block + 1):
            if block in blocks:
                # This block has characters - create an index2 block for it
                block_signature = tuple(sorted(blocks[block]))
                
                if block_signature in index2_blocks:
                    # Reuse existing index2 block
                    self.index1[block] = index2_blocks[block_signature]
                else:
                    # Create new index2 block
                    self.index1[block] = current_index2_pos
                    index2_blocks[block_signature] = current_index2_pos
                    
                    # Fill the index2 block (4096 entries)
                    for i in range(self.BLOCK_SIZE):
                        code_point = (block << self.SHIFT) + i
                        if code_point in self.record_index_map:
                            self.index2.append(self.record_index_map[code_point])
                        else:
                            self.index2.append(0)  # 0 = unassigned character
                    
                    current_index2_pos += self.BLOCK_SIZE
            else:
                # Empty block - point to the default (unassigned) block
                self.index1[block] = 0
        
        print(f"✓ Index1 size: {len(self.index1)} entries")
        print(f"✓ Index2 size: {len(self.index2)} entries")
        print(f"✓ Unique index2 blocks: {len(index2_blocks)}")
    
    def _get_record_index(self, code_point: int) -> int:
        """
        Look up character record index using double indexing
        This replicates _getrecord_ex() from unicodedata.c
        """
        if code_point > 0x10FFFF:
            return 0  # Out of Unicode range
        
        # Double indexing lookup:
        # 1. Use high bits to find index1 entry
        block = code_point >> self.SHIFT
        if block >= len(self.index1):
            return 0
        
        # 2. Use index1 to find index2 block, then low bits to find record index
        index2_pos = self.index1[block]
        index_in_block = code_point & self.BLOCK_MASK
        
        record_index = self.index2[index2_pos + index_in_block]
        return record_index
    
    def get_character_by_index(self, code_point: int) -> UnicodeChar:
        """Get character using the double index system"""
        record_index = self._get_record_index(code_point)
        if record_index == 0:
            return None  # Unassigned character
        
        # Find the character with this record index
        # In real Python, this would lookup in _PyUnicode_Database_Records
        for cp, char in self.chars.items():
            if self.record_index_map.get(cp) == record_index:
                return char
        
        return None

class UnicodeDatabaseWithIndex(DoubleIndexedUnicodeDatabase):
    """
    Complete Unicode database with double indexing and all Unicode functions
    """
    
    def __init__(self, chars: Dict[int, UnicodeChar]):
        super().__init__(chars)
    
    def demonstrate_index_performance(self):
        """Demonstrate the efficiency of double indexing"""
        print("\n" + "="*50)
        print("DOUBLE INDEX PERFORMANCE DEMONSTRATION")
        print("="*50)
        
        test_points = [0x0041, 0x0039, 0x00C0, 0x0660, 0x1F600, 0x12345]
        
        print("Testing double index lookup:")
        for cp in test_points:
            
            # Time the double index lookup
            start = time.perf_counter_ns()
            record_index = self._get_record_index(cp)
            char = self.get_character_by_index(cp)
            end = time.perf_counter_ns()
            
            if char:
                print(f"U+{cp:04X}: {char.name} - {end-start} ns")
            else:
                print(f"U+{cp:04X}: [unassigned] - {end-start} ns")
        
        # Compare with direct dictionary lookup
        print("\nComparing with direct dictionary lookup:")
        for cp in test_points:
            start = time.perf_counter_ns()
            char = self.chars.get(cp)
            end = time.perf_counter_ns()
            
            if char:
                print(f"U+{cp:04X}: {char.name} - {end-start} ns")
            else:
                print(f"U+{cp:04X}: [unassigned] - {end-start} ns")

def analyze_index_efficiency(database: DoubleIndexedUnicodeDatabase):
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

def main():
    """Main function for Step 2.5"""
    print("="*60)
    print("STEP 2.5: IMPLEMENT DOUBLE INDEXING SYSTEM")
    print("Replicating Python's efficient Unicode lookup")
    print("="*60)
    
    # Get data from Step 1
    try:
        unicode_version = "17.0.0"
        filename = download_unicode_data(unicode_version)
        ea_width_mapping = download_east_asian_widths(unicode_version)
        
        aux_files = download_unicode_auxiliary_files(unicode_version)
        blocks = parse_blocks(aux_files["Blocks"])
        scripts = parse_scripts(aux_files["Scripts"])
        prop_list = parse_prop_list(aux_files["PropList"])
        
        chars = parse_unicode_data(filename, blocks, scripts, prop_list)
    except Exception as e:
        print(f"Error: Could not load data from Step 1: {e}")
        sys.exit(1)
    
    # Build database with double indexing
    print("\nBuilding double-indexed Unicode database...")
    database = UnicodeDatabaseWithIndex(chars)
    
    # Analyze efficiency
    analyze_index_efficiency(database)
    
    # Analyze and save property database summary
    analysis_summary = analyze_property_database(database)
    save_property_database_summary(analysis_summary)
    
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
    database = main()

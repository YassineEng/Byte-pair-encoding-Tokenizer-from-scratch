#!/usr/bin/env python3
"""
Unicode Indexing System
Contains the core Unicode character double-indexing mechanism.
"""

from typing import Dict, List, Tuple
import time # Keep time for performance demonstration

# Import from our previous steps
from src.data_preparation.step_02_parse_data import UnicodeChar

class DoubleIndexedUnicodeDatabase(object): # Inherit from object explicitly
    """
    Adds the efficient double-indexing system used by Python's unicodedata
    This is the ACTUAL lookup mechanism from _getrecord_ex() in unicodedata.c
    """
    
    def __init__(self, chars: Dict[int, UnicodeChar]):
        self.chars = chars # Store the raw character data
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
                char.uppercase,
                char.lowercase,
                char.titlecase,
                char.decomposition,
                char.decimal,
                char.digit,
                char.numeric,
                char.unicode1_name,
                char.iso_comment,
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

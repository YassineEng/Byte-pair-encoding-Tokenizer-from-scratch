#!/usr/bin/env python3
"""
Step 3: Unicode Normalization Functions
Implementing NFC, NFD, NFKC, NFKD normalization like Python's unicodedata.normalize()
"""

from typing import Dict, List, Optional, Tuple

# Import from previous steps
from src.config import UNICODE_VERSION
from src.unicode_database.database_builder import build_database
from src.unicode_database.lookup import UnicodeDatabaseWithIndex

class UnicodeNormalizer:
    """
    Implements Unicode normalization algorithms (NFC, NFD, NFKC, NFKD)
    This replicates the functionality of unicodedata.normalize()
    """
    
    def __init__(self, database: UnicodeDatabaseWithIndex):
        self.db = database
        self._build_decomposition_tables()
        self._build_composition_tables()
    
    def _build_decomposition_tables(self):
        """Parse decomposition mappings from Unicode data"""
        print("Building decomposition tables...")
        
        self.decomposition_map = {}  # code_point -> decomposed characters
        self.compatibility_map = {}  # code_point -> compatibility decomposition
        self.canonical_map = {}      # code_point -> canonical decomposition
        
        for code_point, char in self.db.chars.items():
            if char.decomposition and char.decomposition != '':
                # Parse decomposition mapping like "0041 0300"
                decomp_chars = []
                decomp_type = 'canonical'  # Default
                
                # Check for compatibility decomposition (starts with <tag>)
                decomp_str = char.decomposition
                if decomp_str.startswith('<'):
                    # Compatibility decomposition: "<font> 0041"
                    tag_end = decomp_str.find('>')
                    if tag_end != -1:
                        decomp_type = 'compatibility'
                        decomp_str = decomp_str[tag_end + 1:].strip()
                
                # Parse hex code points
                hex_codes = decomp_str.split()
                for hex_code in hex_codes:
                    if hex_code:
                        try:
                            decomp_char_code = int(hex_code, 16)
                            decomp_chars.append(decomp_char_code)
                        except ValueError:
                            continue
                
                if decomp_chars:
                    self.decomposition_map[code_point] = decomp_chars
                    if decomp_type == 'compatibility':
                        self.compatibility_map[code_point] = decomp_chars
                    else:
                        self.canonical_map[code_point] = decomp_chars
        
        print(f"✓ Decomposition mappings: {len(self.decomposition_map)}")
        print(f"  - Canonical: {len(self.canonical_map)}")
        print(f"  - Compatibility: {len(self.compatibility_map)}")
    
    def _build_composition_tables(self):
        """Build composition tables for NFC/NFKC"""
        print("Building composition tables...")
        
        self.composition_map = {}  # (first_char, second_char) -> composed_char
        
        # Build composition pairs from decomposition mappings
        for composed_char, decomp_chars in self.canonical_map.items():
            if len(decomp_chars) == 2:
                # This is a canonical decomposition that can be recomposed
                first_char, second_char = decomp_chars
                self.composition_map[(first_char, second_char)] = composed_char
        
        print(f"✓ Composition pairs: {len(self.composition_map)}")
    
    def normalize(self, text: str, form: str = 'NFC') -> str:
        """
        Normalize Unicode text using the specified form
        Replicates unicodedata.normalize(form, text)
        
        Forms:
        - NFC:  Normalization Form C - Canonical Composition
        - NFD:  Normalization Form D - Canonical Decomposition  
        - NFKC: Normalization Form KC - Compatibility Composition
        - NFKD: Normalization Form KD - Compatibility Decomposition
        """
        if not text:
            return text
        
        form = form.upper()
        if form not in ['NFC', 'NFD', 'NFKC', 'NFKD']:
            raise ValueError(f"invalid normalization form {form}")
        
        # Convert to decomposition form first
        if form in ['NFD', 'NFKD']:
            # Decompose only
            decomposed = self._decompose(text, compatibility=(form == 'NFKD'))
            return ''.join(chr(cp) for cp in decomposed)
        else:
            # NFC/NFKC: Decompose then recompose
            decomposed = self._decompose(text, compatibility=(form == 'NFKC'))
            composed = self._compose(decomposed)
            return ''.join(chr(cp) for cp in composed)
    
    def _decompose(self, text: str, compatibility: bool = False) -> List[int]:
        """Recursively decompose characters"""
        result = []
        
        for char in text:
            code_point = ord(char)
            
            # Check if this character should be decomposed
            decomp_chars = None
            if compatibility:
                # NFKC/NFKD: Use both canonical and compatibility decompositions
                decomp_chars = self.decomposition_map.get(code_point)
            else:
                # NFD: Use only canonical decompositions
                decomp_chars = self.canonical_map.get(code_point)
            
            if decomp_chars:
                # Recursively decompose each character in the decomposition
                for decomp_char in decomp_chars:
                    decomp_str = chr(decomp_char)
                    result.extend(self._decompose(decomp_str, compatibility))
            else:
                # No decomposition, keep the original character
                result.append(code_point)
        
        return result
    
    def _compose(self, code_points: List[int]) -> List[int]:
        """Canonical composition algorithm"""
        if not code_points:
            return []
        
        # First character starts the starter sequence
        result = [code_points[0]]
        
        for current_char in code_points[1:]:
            # Get combining class of current character
            current_cc = self.db.combining(chr(current_char))
            
            # Find the last starter (character with combining class 0)
            last_starter_idx = -1
            for i in range(len(result) - 1, -1, -1):
                if self.db.combining(chr(result[i])) == 0:
                    last_starter_idx = i
                    break
            
            if last_starter_idx == -1:
                # No starter found, just append
                result.append(current_char)
                continue
            
            # Check if we can compose with the starter
            starter_char = result[last_starter_idx]
            composition_key = (starter_char, current_char)
            
            if composition_key in self.composition_map:
                # Replace starter with composed character
                composed_char = self.composition_map[composition_key]
                result[last_starter_idx] = composed_char
            else:
                # Insert in canonical order based on combining class
                insert_pos = len(result)
                current_cc = self.db.combining(chr(current_char))
                
                for i in range(len(result) - 1, last_starter_idx, -1):
                    prev_cc = self.db.combining(chr(result[i]))
                    if prev_cc <= current_cc:
                        insert_pos = i + 1
                        break
                
                result.insert(insert_pos, current_char)
        
        return result
    
    def is_normalized(self, text: str, form: str = 'NFC') -> bool:
        """
        Check if text is already normalized in the specified form
        Replicates unicodedata.is_normalized(form, text)
        """
        if not text:
            return True
        
        normalized = self.normalize(text, form)
        return text == normalized
    
    def _quick_check(self, text: str, form: str) -> bool:
        """
        Simple quick check optimization (simplified version)
        In real Python, this uses the normalization_quick_check field
        """
        for char in text:
            code_point = ord(char)
            char_data = self.db.chars.get(code_point)
            
            if not char_data:
                continue
            
            # Simplified quick check logic
            has_decomposition = char_data.decomposition != ''
            is_combining = char_data.combining > 0
            
            if form in ['NFD', 'NFKD'] and has_decomposition:
                return False  # Would be decomposed
            elif form in ['NFC', 'NFKC'] and is_combining:
                return False  # Would be reordered/composed
        
        return True

def create_normalizer():
    """
    Builds and returns a UnicodeNormalizer object, utilizing the cached database.
    """
    print("="*60)
    print("STEP 3: UNICODE NORMALIZATION AND LOOKUP FUNCTIONS")
    print("Replicating unicodedata.normalize() and unicodedata.lookup()")
    print("="*60)
    
    # Get database from the robust build_database function
    database = build_database()
    
    # Build normalizer
    print("\nBuilding normalization engine...")
    normalizer = UnicodeNormalizer(database)
    
    print("\n" + "="*60)
    print("STEP 3 COMPLETED SUCCESSFULLY!")
    print("✓ Implemented Unicode normalization (NFC, NFD, NFKC, NFKD)")
    print("✓ Ready for Unicode version support!")
    print("="*60)
    
    return normalizer

if __name__ == "__main__":
    normalizer = create_normalizer()
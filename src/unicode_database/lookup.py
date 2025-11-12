#!/usr/bin/env python3
"""
Unicode Lookup Functions
Provides functions to access Unicode character properties using the indexing system.
"""

from typing import Dict, List, Tuple, Optional, Union
import time # Keep time for performance demonstration

# Import from our previous steps
from src.data_preparation.parse_data import UnicodeChar
from src.unicode_database.indexing import DoubleIndexedUnicodeDatabase

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
        
        test_points = [0x0041, 0x0039, 0x00C0] # Simplified test points
        
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
    
    def name(self, char_or_code_point: Union[str, int], default: Optional[str] = None) -> Optional[str]:
        """
        Returns the name of the character.
        If the character is not defined, returns default or raises ValueError.
        """
        code_point = ord(char_or_code_point) if isinstance(char_or_code_point, str) else char_or_code_point
        char_data = self.get_character_by_index(code_point)
        if char_data and char_data.name:
            return char_data.name
        if default is not None:
            return default
        raise ValueError(f"Character U+{code_point:04X} has no name defined.")

    def category(self, char_or_code_point: Union[str, int]) -> str:
        """
        Returns the general category of the character.
        """
        code_point = ord(char_or_code_point) if isinstance(char_or_code_point, str) else char_or_code_point
        char_data = self.get_character_by_index(code_point)
        return char_data.category if char_data else 'Cn' # 'Cn' for unassigned

    def decimal(self, char_or_code_point: Union[str, int], default: Optional[int] = None) -> Optional[int]:
        """
        Returns the decimal value of the character.
        If not a decimal character, returns default or raises ValueError.
        """
        code_point = ord(char_or_code_point) if isinstance(char_or_code_point, str) else char_or_code_point
        char_data = self.get_character_by_index(code_point)
        if char_data and char_data.decimal is not None:
            return char_data.decimal
        if default is not None:
            return default
        raise ValueError(f"Character U+{code_point:04X} is not a decimal character.")

    def digit(self, char_or_code_point: Union[str, int], default: Optional[int] = None) -> Optional[int]:
        """
        Returns the digit value of the character.
        If not a digit character, returns default or raises ValueError.
        """
        code_point = ord(char_or_code_point) if isinstance(char_or_code_point, str) else char_or_code_point
        char_data = self.get_character_by_index(code_point)
        if char_data and char_data.digit is not None:
            return char_data.digit
        if default is not None:
            return default
        raise ValueError(f"Character U+{code_point:04X} is not a digit character.")

    def numeric(self, char_or_code_point: Union[str, int], default: Optional[float] = None) -> Optional[float]:
        """
        Returns the numeric value of the character as a float.
        If not a numeric character, returns default or raises ValueError.
        """
        code_point = ord(char_or_code_point) if isinstance(char_or_code_point, str) else char_or_code_point
        char_data = self.get_character_by_index(code_point)
        if char_data and char_data.numeric:
            try:
                # Handle fractions like "1/2"
                if '/' in char_data.numeric:
                    num, den = map(int, char_data.numeric.split('/'))
                    return float(num) / den
                return float(char_data.numeric)
            except ValueError:
                pass # Fall through to default/error
        if default is not None:
            return default
        raise ValueError(f"Character U+{code_point:04X} is not a numeric character.")

    def combining(self, char_or_code_point: Union[str, int]) -> int:
        """
        Returns the canonical combining class for the character.
        """
        code_point = ord(char_or_code_point) if isinstance(char_or_code_point, str) else char_or_code_point
        char_data = self.get_character_by_index(code_point)
        return char_data.combining if char_data else 0

    def bidirectional(self, char_or_code_point: Union[str, int]) -> str:
        """
        Returns the bidirectional class for the character.
        """
        code_point = ord(char_or_code_point) if isinstance(char_or_code_point, str) else char_or_code_point
        char_data = self.get_character_by_index(code_point)
        return char_data.bidirectional if char_data else 'L' # 'L' for unassigned (Left-to-Right)

    def mirrored(self, char_or_code_point: Union[str, int]) -> int:
        """
        Returns 1 if the character is mirrored in bidirectional text, 0 otherwise.
        """
        code_point = ord(char_or_code_point) if isinstance(char_or_code_point, str) else char_or_code_point
        char_data = self.get_character_by_index(code_point)
        return 1 if char_data and char_data.mirrored == 'Y' else 0

    def decomposition(self, char_or_code_point: Union[str, int]) -> str:
        """
        Returns the decomposition mapping for the character.
        """
        code_point = ord(char_or_code_point) if isinstance(char_or_code_point, str) else char_or_code_point
        char_data = self.get_character_by_index(code_point)
        return char_data.decomposition if char_data else ''

    def is_mirrored(self, char_or_code_point: Union[str, int]) -> bool:
        """
        Checks if the character has the Bidi_Mirrored property.
        """
        return self.mirrored(char_or_code_point) == 1

    def lookup(self, name: str) -> str:
        """
        Looks up a character by its official Unicode name.
        This is a simplified implementation for demonstration.
        """
        # This would be very inefficient for a full database.
        # A real implementation would use a name alias table or a hash map.
        for cp, char_data in self.chars.items():
            if char_data.name == name:
                return chr(cp)
        raise KeyError(f"Character with name '{name}' not found.")

    def normalize(self, form: str, text: str) -> str:
        """
        Returns the normal form 'form' for the Unicode string 'text'.
        This is a placeholder and would require a full normalization algorithm.
        """
        # This is a complex algorithm (NFC, NFD, NFKC, NFKD)
        # For now, we'll just return the text as is.
        print(f"Warning: Normalization form '{form}' is not fully implemented. Returning original text.")
        return text

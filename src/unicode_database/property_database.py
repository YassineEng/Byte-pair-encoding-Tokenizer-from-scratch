#!/usr/bin/env python3
"""
Simplified Unicode Property Database
Provides basic Unicode character property access for the simplified scope.
"""

from typing import Dict, List, Optional
from src.data_preparation.download_parse import UnicodeChar

class UnicodePropertyDatabase:
    """
    Provides access to Unicode character properties.
    Simplified for English, numbers, and punctuation scope.
    """
    
    def __init__(self, chars: Dict[int, UnicodeChar]):
        self.chars = chars
    
    def _get_char_data(self, char: str) -> Optional[UnicodeChar]:
        """Helper to get UnicodeChar data for a given character."""
        if not char or len(char) != 1:
            return None
        return self.chars.get(ord(char))

    def name(self, char: str, default: str = '') -> str:
        """Returns the official Unicode name of the character."""
        char_data = self._get_char_data(char)
        return char_data.name if char_data else default

    def category(self, char: str, default: str = '') -> str:
        """Returns the general category of the character."""
        char_data = self._get_char_data(char)
        return char_data.category if char_data else default

    def combining(self, char: str, default: int = 0) -> int:
        """Returns the canonical combining class of the character."""
        char_data = self._get_char_data(char)
        return char_data.combining if char_data else default

    def bidirectional(self, char: str, default: str = '') -> str:
        """Returns the bidirectional category of the character."""
        char_data = self._get_char_data(char)
        return char_data.bidirectional if char_data else default

    def decomposition(self, char: str, default: str = '') -> str:
        """Returns the decomposition mapping of the character."""
        char_data = self._get_char_data(char)
        return char_data.decomposition if char_data else default

    def decimal(self, char: str, default: Optional[int] = None) -> Optional[int]:
        """Returns the decimal value of the character if it's a decimal digit."""
        char_data = self._get_char_data(char)
        return char_data.decimal if char_data else default

    def digit(self, char: str, default: Optional[int] = None) -> Optional[int]:
        """Returns the digit value of the character if it's a digit."""
        char_data = self._get_char_data(char)
        return char_data.digit if char_data else default

    def numeric(self, char: str, default: Optional[str] = None) -> Optional[str]:
        """Returns the numeric value of the character if it has one."""
        char_data = self._get_char_data(char)
        return char_data.numeric if char_data else default

    def mirrored(self, char: str, default: str = 'N') -> str:
        """Returns 'Y' if the character is mirrored in bidirectional text, 'N' otherwise."""
        char_data = self._get_char_data(char)
        return char_data.mirrored if char_data else default

    def unicode1_name(self, char: str, default: str = '') -> str:
        """Returns the Unicode 1.0 name of the character."""
        char_data = self._get_char_data(char)
        return char_data.unicode1_name if char_data else default

    def iso_comment(self, char: str, default: str = '') -> str:
        """Returns the ISO 10646 comment for the character."""
        char_data = self._get_char_data(char)
        return char_data.iso_comment if char_data else default

    def uppercase(self, char: str, default: Optional[int] = None) -> Optional[int]:
        """Returns the code point of the uppercase mapping."""
        char_data = self._get_char_data(char)
        return char_data.uppercase if char_data else default

    def lowercase(self, char: str, default: Optional[int] = None) -> Optional[int]:
        """Returns the code point of the lowercase mapping."""
        char_data = self._get_char_data(char)
        return char_data.lowercase if char_data else default

    def titlecase(self, char: str, default: Optional[int] = None) -> Optional[int]:
        """Returns the code point of the titlecase mapping."""
        char_data = self._get_char_data(char)
        return char_data.titlecase if char_data else default

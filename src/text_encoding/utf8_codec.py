#!/usr/bin/env python3
"""
Custom UTF-8 Encoder/Decoder
Replicates Python's str.encode('utf-8') and bytes.decode('utf-8')
"""

import sys
from typing import List

class CustomUTF8Codec:
    """
    Custom UTF-8 encoder and decoder
    Replicates Python's str.encode('utf-8') and bytes.decode('utf-8')
    """
    
    @staticmethod
    def encode(text: str) -> List[int]:
        """
        Encode Unicode string to UTF-8 bytes (as integers 0-255)
        """
        bytes_list = []
        
        for char in text:
            code_point = ord(char)
            bytes_list.extend(CustomUTF8Codec._encode_code_point(code_point))
        
        return bytes_list
    
    @staticmethod
    def _encode_code_point(code_point: int) -> List[int]:
        """Encode a single Unicode code point to UTF-8 bytes"""
        
        if code_point <= 0x7F:
            # 1 byte: 0xxxxxxx
            return [code_point]
        
        elif code_point <= 0x7FF:
            # 2 bytes: 110xxxxx 10xxxxxx
            byte1 = 0b11000000 | (code_point >> 6)
            byte2 = 0b10000000 | (code_point & 0b00111111)
            return [byte1, byte2]
        
        elif code_point <= 0xFFFF:
            # 3 bytes: 1110xxxx 10xxxxxx 10xxxxxx
            byte1 = 0b11100000 | (code_point >> 12)
            byte2 = 0b10000000 | ((code_point >> 6) & 0b00111111)
            byte3 = 0b10000000 | (code_point & 0b00111111)
            return [byte1, byte2, byte3]
        
        elif code_point <= 0x10FFFF:
            # 4 bytes: 11110xxx 10xxxxxx 10xxxxxx 10xxxxxx
            byte1 = 0b11110000 | (code_point >> 18)
            byte2 = 0b10000000 | ((code_point >> 12) & 0b00111111)
            byte3 = 0b10000000 | ((code_point >> 6) & 0b00111111)
            byte4 = 0b10000000 | (code_point & 0b00111111)
            return [byte1, byte2, byte3, byte4]
        
        else:
            raise ValueError(f"Invalid Unicode code point: U+{code_point:04X}")
    
    @staticmethod
    def decode(bytes_list: List[int]) -> str:
        """
        Decode UTF-8 bytes back to Unicode string
        """
        text = ""
        i = 0
        
        while i < len(bytes_list):
            byte = bytes_list[i]
            
            # Determine how many bytes this character uses
            if (byte & 0b10000000) == 0b00000000:
                # 1-byte character: 0xxxxxxx
                code_point = byte
                bytes_used = 1
                
            elif (byte & 0b11100000) == 0b11000000:
                # 2-byte character: 110xxxxx 10xxxxxx
                if i + 1 >= len(bytes_list):
                    raise ValueError("Incomplete UTF-8 sequence")
                code_point = ((byte & 0b00011111) << 6) | (bytes_list[i + 1] & 0b00111111)
                bytes_used = 2
                
            elif (byte & 0b11110000) == 0b11100000:
                # 3-byte character: 1110xxxx 10xxxxxx 10xxxxxx
                if i + 2 >= len(bytes_list):
                    raise ValueError("Incomplete UTF-8 sequence")
                code_point = ((byte & 0b00001111) << 12) | \
                            ((bytes_list[i + 1] & 0b00111111) << 6) | \
                            (bytes_list[i + 2] & 0b00111111)
                bytes_used = 3
                
            elif (byte & 0b11111000) == 0b11110000:
                # 4-byte character: 11110xxx 10xxxxxx 10xxxxxx 10xxxxxx
                if i + 3 >= len(bytes_list):
                    raise ValueError("Incomplete UTF-8 sequence")
                code_point = ((byte & 0b00000111) << 18) | \
                            ((bytes_list[i + 1] & 0b00111111) << 12) | \
                            ((bytes_list[i + 2] & 0b00111111) << 6) | \
                            (bytes_list[i + 3] & 0b00111111)
                bytes_used = 4
                
            else:
                raise ValueError(f"Invalid UTF-8 byte: 0x{byte:02x}")
            
            # Validate the code point
            if code_point > 0x10FFFF or (0xD800 <= code_point <= 0xDFFF):
                raise ValueError(f"Invalid Unicode code point: U+{code_point:04X}")
            
            text += chr(code_point)
            i += bytes_used
        
        return text

#!/usr/bin/env python3
"""
Utility function to get byte pairs for the BPE Tokenizer.
"""

from typing import List, Tuple, Dict
from collections import defaultdict

def get_byte_pairs(tokens: List[int]) -> Dict[Tuple[int, int], int]:
    """Counts the frequency of consecutive byte pairs in a list of tokens."""
    pairs = defaultdict(int)
    for i in range(len(tokens) - 1):
        pairs[(tokens[i], tokens[i+1])] += 1
    return pairs

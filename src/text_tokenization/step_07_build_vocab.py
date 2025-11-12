#!/usr/bin/env python3
"""
Utility function to build the initial vocabulary for the BPE Tokenizer.
"""

from typing import Tuple, Dict

def build_initial_vocab() -> Tuple[Dict[bytes, int], Dict[int, bytes]]:
    """
    Builds the initial vocabulary of 256 bytes plus special tokens.
    Returns two dictionaries: one mapping byte sequences to token IDs,
    and another mapping token IDs back to byte sequences.
    """
    vocab = {}
    token_to_bytes = {}
    next_token_id = 0

    # Special tokens
    special_tokens = {
        b'<|endoftext|>': next_token_id,
        b'<|unk|>': next_token_id + 1,
    }
    next_token_id += len(special_tokens)

    for token_bytes, token_id in special_tokens.items():
        vocab[token_bytes] = token_id
        token_to_bytes[token_id] = token_bytes

    # Add all 256 byte tokens
    for byte_val in range(256):
        byte_seq = bytes([byte_val])
        vocab[byte_seq] = next_token_id
        token_to_bytes[next_token_id] = byte_seq
        next_token_id += 1
        
    return vocab, token_to_bytes

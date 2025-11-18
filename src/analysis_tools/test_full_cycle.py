#!/usr/bin/env python3
"""
Test script to verify the full BPE encoding and decoding cycle.
"""

import json
import os
from src.step_07_utf8_codec import CustomUTF8Codec
from src.config import BPE_TRAINING_CORPUS

def test_full_cycle():
    """
    Tests that the tokens generated from the BPE corpus can be decoded
    back to the original text.
    """
    print("=" * 80)
    print("Testing Full BPE Encode/Decode Cycle")
    print("=" * 80)

    output_dir = "outputs"
    tokens_path = os.path.join(output_dir, "output_tokens.txt")
    vocab_path = os.path.join(output_dir, "vocab_bytes.json") # Use the lossless vocab

    # --- 1. Load the vocabulary ---
    print(f"Loading vocabulary from {vocab_path}...")
    try:
        with open(vocab_path, 'r', encoding='utf-8') as f:
            vocab_json = json.load(f)
    except FileNotFoundError:
        print(f"Error: Vocabulary file not found at {vocab_path}")
        print("Please run step_11_main.py to generate the vocabulary and tokens.")
        return
    
    # Convert string keys back to int and byte lists back to bytes
    vocab_map = {
        int(token_id_str): bytes(byte_list) 
        for token_id_str, byte_list in vocab_json.items()
    }
    print(f"✓ Vocabulary loaded with {len(vocab_map)} entries.")

    # --- 2. Load the tokens ---
    print(f"Loading tokens from {tokens_path}...")
    try:
        with open(tokens_path, 'r', encoding='utf-8') as f:
            token_ids_str = f.read().strip().split()
            token_ids = [int(tid) for tid in token_ids_str]
    except FileNotFoundError:
        print(f"Error: Tokens file not found at {tokens_path}")
        print("Please run step_11_main.py to generate the vocabulary and tokens.")
        return
    print(f"✓ Loaded {len(token_ids)} tokens.")

    # --- 3. Decode the tokens ---
    print("Decoding token sequence...")
    decoded_bytes_list = []
    for token_id in token_ids:
        # Use .get() to handle potential unknown tokens gracefully
        decoded_bytes_list.append(vocab_map.get(token_id, b'<|unk|>'))
    
    full_byte_sequence = b''.join(decoded_bytes_list)
    
    # The custom codec expects a list of integer byte values
    decoded_text = CustomUTF8Codec.decode(list(full_byte_sequence))
    print("✓ Decoding complete.")

    # --- 4. Prepare the original corpus for comparison ---
    # The encoding process encodes each line separately. We join them back to compare.
    original_text_processed = "".join([line for line in BPE_TRAINING_CORPUS.strip().split('\n') if line.strip()])
    
    # --- 5. Compare and verify ---
    print("Comparing decoded text with the original corpus...")
    
    if decoded_text != original_text_processed:
        print("\n--- MISMATCH DETECTED ---")
        print("\nOriginal Processed Text:")
        print(repr(original_text_processed))
        print("\nDecoded Text:")
        print(repr(decoded_text))
        print("\n--- END MISMATCH ---")

    assert decoded_text == original_text_processed, "Mismatch between original corpus and decoded text!"
    
    print("\n✓ SUCCESS: Decoded text perfectly matches the original BPE training corpus.")
    print("=" * 80)

if __name__ == "__main__":
    test_full_cycle()
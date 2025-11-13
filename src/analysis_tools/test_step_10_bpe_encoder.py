#!/usr/bin/env python3
"""
Analysis and testing script for the BPE encoder (Step 10).
"""

from typing import List, Tuple, Dict
from collections import defaultdict

# Import from our custom modules
from src.step_10_bpe_encoder import CustomBPEEncoder
from src.step_06_normalizer import UnicodeNormalizer, create_normalizer
from src.config import BPE_NUM_MERGES

def demonstrate_bpe(normalizer: UnicodeNormalizer):
    """Demonstrate BPE training, encoding, and decoding"""
    print("\n" + "=" * 50)
    print("BPE TRAINING AND ENCODING/DECODING DEMONSTRATION")
    print("=" * 50)

    # This corpus is simplified to use only characters within the allowed ranges
    corpus = [
        "low", "lower", "newest", "widest", "hello world", "hello world wide web",
        "apple", "apply", "application", "banana", "bandana", "band",
        "normalization test", "café", "résumé",
    ]
    
    print(f"\nTraining BPE on corpus of {len(corpus)} documents with {BPE_NUM_MERGES} merges...")
    bpe_encoder = CustomBPEEncoder(normalizer)
    bpe_encoder.train(BPE_NUM_MERGES)

    print("\n" + "=" * 50)
    print("BPE VOCABULARY AND MERGES")
    print("=" * 50)
    
def sanitize_for_display(byte_seq: bytes) -> str:
    """Create a display-safe version of a byte sequence."""
    try:
        # Try to decode, but replace special characters with their escaped versions
        return byte_seq.decode('utf-8', errors='replace') \
            .replace('\n', '\\n') \
            .replace('\r', '\\r') \
            .replace('\t', '\\t')
    except Exception:
        return str(byte_seq)

    print("\nVocabulary (Token ID -> Bytes):")
    token_to_bytes = bpe_encoder.get_vocab_info()
    sorted_vocab_items = sorted(token_to_bytes.items(), key=lambda item: item[0])
    for token_id, byte_seq in sorted_vocab_items:
        display_str = sanitize_for_display(byte_seq)
        print(f"  {token_id}: {byte_seq} ('{display_str}')")

    print("\nMerges (Pair of Token IDs -> New Token ID):")
    merges = bpe_encoder.get_merges_info()
    sorted_merges_items = sorted(merges.items(), key=lambda item: item[1])
    for (t1, t2), new_id in sorted_merges_items:
        s1 = sanitize_for_display(token_to_bytes[t1])
        s2 = sanitize_for_display(token_to_bytes[t2])
        new_s = sanitize_for_display(token_to_bytes[new_id])
        print(f"  ({t1} '{s1}', {t2} '{s2}') -> {new_id} ('{new_s}')")

    print("\n" + "=" * 50)
    print("BPE ENCODING/DECODING EXAMPLES")
    print("=" * 50)

    test_texts = [
        "lower",
        "newest",
        "hello world wide web",
        "application",
        "café",
        "This is a test sentence for BPE encoding.",
        "A new word that wasn't in the corpus."
    ]

    for text in test_texts:
        print(f"\nOriginal Text: '{text}'")
        
        encoded_tokens = bpe_encoder.encode(text)
        decoded_text = bpe_encoder.decode(encoded_tokens)
        
        print(f"  Encoded Tokens: {encoded_tokens}")
        
        # Display token IDs with their byte representations
        token_display = []
        for token_id in encoded_tokens:
            byte_seq = bpe_encoder.token_to_bytes.get(token_id, b'<|unk|>')
            display_str = sanitize_for_display(byte_seq)
            token_display.append(f"{token_id} ('{display_str}')")
        print(f"  Token Representations: [{', '.join(token_display)}]")

        print(f"  Decoded Text: '{decoded_text}'")
        
        # Compare with normalized original text
        normalized_original = normalizer.normalize(text)
        success = (decoded_text == normalized_original)
        print(f"  Round-trip Success (vs normalized original): {success}")
        if not success:
            print(f"  Normalized Original: '{normalized_original}'")

if __name__ == "__main__":
    print("Initializing Unicode Normalizer for BPE demonstration...")
    normalizer = create_normalizer()
    demonstrate_bpe(normalizer)

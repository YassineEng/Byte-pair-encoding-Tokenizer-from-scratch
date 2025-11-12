#!/usr/bin/env python3
"""
Step 4.5: Demonstrate Custom UTF-8 Encoder/Decoder and BPE
"""

from typing import List, Tuple, Dict

# Import from our custom modules
from src.text_encoding.utf8_codec import CustomUTF8Codec
from src.text_tokenization.bpe_encoder import CustomBPEEncoder
from src.unicode_processing.normalizer import UnicodeNormalizer, create_normalizer

def demonstrate_custom_utf8():
    """
    Test our custom UTF-8 encoder/decoder.
    NOTE: The test cases are limited to characters within the ALLOWED_RANGES
    defined in parse_data.py (e.g., Basic Latin, Latin-1 Supplement) to
    reflect the current simplified scope of the project.
    """
    print("CUSTOM UTF-8 ENCODER/DECODER TEST")
    print("=" * 50)
    
    test_cases = [
        "A",           # Basic ASCII (1 byte)
        "é",           # Latin-1 (2 bytes)
        "€",           # A 3-byte character from the Currency Symbols block
        "Hello, world!", # Mixed ASCII
        "café résumé", # Mixed Latin-1
    ]
    
    for text in test_cases:
        print(f"\nText: '{text}'")
        
        # Our custom encoding
        custom_bytes = CustomUTF8Codec.encode(text)
        custom_decoded = CustomUTF8Codec.decode(custom_bytes)
        
        # Python's built-in encoding (for comparison)
        python_bytes = list(text.encode('utf-8'))
        python_decoded = bytes(python_bytes).decode('utf-8')
        
        print(f"  Code points: {[f'U+{ord(c):04X}' for c in text]}")
        print(f"  Custom bytes: {custom_bytes}")
        print(f"  Python bytes: {python_bytes}")
        print(f"  Bytes match: {custom_bytes == python_bytes}")
        print(f"  Custom decoded: '{custom_decoded}'")
        print(f"  Round-trip works: {custom_decoded == text}")

def compare_with_python_builtin():
    """Compare our implementation with Python's built-in functions"""
    print("\n" + "=" * 50)
    print("COMPARISON WITH PYTHON BUILT-IN")
    print("=" * 50)
    
    test_strings = ["A", "é", "€", "café", "Hello, world!"]
    
    for text in test_strings:
        print(f"\n'{text}':")
        
        # Our implementation
        our_bytes = CustomUTF8Codec.encode(text)
        our_decoded = CustomUTF8Codec.decode(our_bytes)
        
        # Python's implementation  
        python_bytes = list(text.encode('utf-8'))
        python_decoded = bytes(python_bytes).decode('utf-8')
        
        print(f"  Our bytes:    {our_bytes}")
        print(f"  Python bytes: {python_bytes}")
        print(f"  Match: {our_bytes == python_bytes}")
        print(f"  Our decode: '{our_decoded}'")
        print(f"  Python decode: '{python_decoded}'")
        print(f"  Both work: {our_decoded == python_decoded == text}")

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
    
    target_vocab_size = 300 # Initial vocab is 258 (2 special + 256 bytes) 
    
    print(f"\nTraining BPE on corpus of {len(corpus)} documents with target vocab size {target_vocab_size}...")
    bpe_encoder = CustomBPEEncoder(normalizer)
    bpe_encoder.train(corpus, target_vocab_size)

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


def main():
    """Main function for Step 4.5"""
    print("=" * 60)
    print("STEP 4.5: BUILD CUSTOM UTF-8 ENCODER/DECODER AND BPE")
    print("Complete control over text → bytes → tokens conversion")
    print("=" * 60)
    
    # Get normalizer from step 3
    try:
        print("Initializing Unicode Normalizer...")
        normalizer = create_normalizer() # Only returns normalizer now
        print("Unicode Normalizer initialized.")
    except Exception as e:
        print(f"Error initializing normalizer: {e}")
        print("Falling back to a simple pass-through normalizer.")
        class SimpleNormalizer:
            def normalize(self, text):
                return text
        normalizer = SimpleNormalizer()
    
    # Test our custom UTF-8 implementation
    demonstrate_custom_utf8()
    
    # Compare with Python's built-in
    compare_with_python_builtin()
    
    # Demonstrate BPE training, encoding, and decoding
    demonstrate_bpe(normalizer)
    
    print("\n" + "=" * 60)
    print("STEP 4.5 COMPLETED SUCCESSFULLY!")
    print("✓ Built custom UTF-8 encoder/decoder")
    print("✓ Implemented BPE training, encoding, and decoding")
    print("✓ Understand byte-level text representation and tokenization") 
    print("=" * 60)

if __name__ == "__main__":
    main()
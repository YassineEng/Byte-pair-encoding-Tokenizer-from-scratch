#!/usr/bin/env python3
"""
Analysis and testing script for step_08_build_vocab.py.
Verifies the functionality of building the initial BPE vocabulary.
"""

from src.step_08_build_vocab import build_initial_vocab

def test_build_initial_vocab():
    """
    Tests the build_initial_vocab function.
    """
    print("\n" + "=" * 50)
    print("TESTING STEP 08: BUILD INITIAL BPE VOCABULARY")
    print("=" * 50)

    try:
        vocab, token_to_bytes = build_initial_vocab()
        print("✓ Initial vocabulary built successfully.")
        print(f"  Total vocabulary size: {len(vocab)}")
        
        # Expected size: 256 bytes + 2 special tokens = 258
        expected_size = 258
        print(f"  Expected size: {expected_size}")
        assert len(vocab) == expected_size, f"Expected vocab size {expected_size}, got {len(vocab)}"
        assert len(token_to_bytes) == expected_size, f"Expected token_to_bytes size {expected_size}, got {len(token_to_bytes)}"

        print("\nSample of vocabulary (Token ID -> Bytes):")
        # Print first 5 and last 5 entries
        sorted_items = sorted(token_to_bytes.items())
        for i, (token_id, byte_seq) in enumerate(sorted_items):
            if i < 5 or i >= len(sorted_items) - 5:
                print(f"  {token_id}: {byte_seq} ('{byte_seq.decode('utf-8', errors='replace')}')")
            elif i == 5:
                print("  ...")

        # Check special tokens
        assert b'<|endoftext|>' in vocab, "Special token <|endoftext|> not in vocab."
        assert b'<|unk|>' in vocab, "Special token <|unk|> not in vocab."
        print("✓ Special tokens found in vocabulary.")

        # Check a few byte values
        assert bytes([0]) in vocab, "Byte 0 not in vocab."
        assert bytes([255]) in vocab, "Byte 255 not in vocab."
        print("✓ All 256 byte values appear to be in vocabulary.")

        print("\n" + "=" * 50)
        print("STEP 08 TEST COMPLETED SUCCESSFULLY!")
        print("=" * 50)

    except Exception as e:
        print(f"✗ An error occurred during initial vocabulary test: {e}")
        print("\n" + "=" * 50)
        print("STEP 08 TEST FAILED!")
        print("=" * 50)

if __name__ == "__main__":
    test_build_initial_vocab()

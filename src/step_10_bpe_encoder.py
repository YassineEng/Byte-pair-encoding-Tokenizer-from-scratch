#!/usr/bin/env python3
"""
Step 4.5: BPE Core Logic
For complete understanding of BPE at the byte level
"""

from typing import List, Tuple, Dict
from collections import defaultdict

from src.step_07_utf8_codec import CustomUTF8Codec
from src.step_08_build_vocab import build_initial_vocab
from src.step_09_get_pairs import get_byte_pairs
from src.config import BPE_TRAINING_CORPUS, BPE_NUM_MERGES

class CustomBPEEncoder:
    """
    BPE encoder using our custom UTF-8 functions
    """
    
    def __init__(self, normalizer):
        self.normalizer = normalizer
        self.merges: Dict[Tuple[int, int], int] = {} # Maps (token_id1, token_id2) to new_token_id
        self.inverse_merges: Dict[int, Tuple[int, int]] = {} # Maps new_token_id to (token_id1, token_id2)
        
        # Initialize vocab and token_to_bytes from the utility function
        self.vocab, self.token_to_bytes = build_initial_vocab()
        self.next_token_id = len(self.vocab)
        
        print(f"Initial vocabulary size: {len(self.vocab)}")
    
    def train(self, num_merges: int):
        """
        Trains the BPE encoder on the configured text corpus to build the vocabulary.
        """
        if num_merges < 0:
            print("Warning: num_merges cannot be negative. No merges will be performed.")
            return

        print(f"Starting BPE training with target number of merges: {num_merges}")
        
        # 1. Pre-tokenize the corpus into initial byte tokens
        tokenized_corpus: List[List[int]] = []
        for text in BPE_TRAINING_CORPUS.strip().split('\n'):
            normalized_text = self.normalizer.normalize(text)
            bytes_list = CustomUTF8Codec.encode(normalized_text)
            
            initial_tokens = [self.vocab[bytes([b])] for b in bytes_list]
            tokenized_corpus.append(initial_tokens)
        
        print(f"Corpus pre-tokenized into {len(tokenized_corpus)} documents.")

        # 2. Iteratively find and merge the most frequent pairs
        while len(self.merges) < num_merges:
            all_pairs = defaultdict(int)
            for doc_tokens in tokenized_corpus:
                pairs_in_doc = get_byte_pairs(doc_tokens)
                for pair, count in pairs_in_doc.items():
                    all_pairs[pair] += count
            
            if not all_pairs:
                print("No more pairs to merge. Stopping training.")
                break
            
            best_pair = max(all_pairs, key=all_pairs.get)
            
            new_token_id = self.next_token_id
            self.next_token_id += 1
            
            token1_bytes = self.token_to_bytes[best_pair[0]]
            token2_bytes = self.token_to_bytes[best_pair[1]]
            new_token_bytes = token1_bytes + token2_bytes
            
            self.vocab[new_token_bytes] = new_token_id
            self.token_to_bytes[new_token_id] = new_token_bytes
            self.merges[best_pair] = new_token_id
            self.inverse_merges[new_token_id] = best_pair
            
            print(f"Merge {len(self.merges)}: {best_pair} -> {new_token_id} (bytes: {new_token_bytes}) (Freq: {all_pairs[best_pair]})")
            
            new_tokenized_corpus = []
            for doc_tokens in tokenized_corpus:
                merged_doc_tokens = []
                i = 0
                while i < len(doc_tokens):
                    if i + 1 < len(doc_tokens) and (doc_tokens[i], doc_tokens[i+1]) == best_pair:
                        merged_doc_tokens.append(new_token_id)
                        i += 2
                    else:
                        merged_doc_tokens.append(doc_tokens[i])
                        i += 1
                new_tokenized_corpus.append(merged_doc_tokens)
            tokenized_corpus = new_tokenized_corpus
            
            if len(self.merges) % 10 == 0: # Print progress every 10 merges
                print(f"  Current merges: {len(self.merges)}/{num_merges}")
        
        print(f"BPE training complete. Final vocab size: {len(self.vocab)}")
        print(f"Total merges learned: {len(self.merges)}")

    def encode(self, text: str) -> List[int]:
        """
        Encodes a text string into a list of BPE token IDs.
        """
        normalized_text = self.normalizer.normalize(text)
        bytes_list = CustomUTF8Codec.encode(normalized_text)
        
        tokens = [self.vocab[bytes([b])] for b in bytes_list]
        
        while True:
            current_pairs = get_byte_pairs(tokens)
            
            best_pair_to_merge = None
            for pair, new_token_id in self.merges.items():
                if pair in current_pairs:
                    if best_pair_to_merge is None or self.merges[best_pair_to_merge] > new_token_id:
                        best_pair_to_merge = pair
            
            if best_pair_to_merge is None:
                break
            
            new_tokens = []
            i = 0
            while i < len(tokens):
                if i + 1 < len(tokens) and (tokens[i], tokens[i+1]) == best_pair_to_merge:
                    new_tokens.append(self.merges[best_pair_to_merge])
                    i += 2
                else:
                    new_tokens.append(tokens[i])
                    i += 1
            tokens = new_tokens
            
        return tokens

    def decode(self, tokens: List[int]) -> str:
        """
        Decodes a list of BPE token IDs back into a text string.
        """
        byte_sequence = []
        for token_id in tokens:
            byte_sequence.extend(list(self.token_to_bytes.get(token_id, b'<|unk|>')))
        
        return CustomUTF8Codec.decode(byte_sequence)

    def get_vocab_info(self) -> Dict[int, bytes]:
        """Returns the current vocabulary mapping token IDs to byte sequences."""
        return self.token_to_bytes
    
    def get_merges_info(self) -> Dict[Tuple[int, int], int]:
        """Returns the learned merge rules."""
        return self.merges

def demonstrate_bpe(normalizer):
    """
    Demonstrates the BPE training and encoding/decoding process.
    """
    print("\n==================================================")
    print("BPE TRAINING AND ENCODING/DECODING DEMONSTRATION")
    print("==================================================")

    encoder = CustomBPEEncoder(normalizer)
    
    print(f"\nTraining BPE on corpus with {BPE_NUM_MERGES} merges...")
    encoder.train(BPE_NUM_MERGES)
    
    print(f"Corpus pre-tokenized into {len(BPE_TRAINING_CORPUS.strip().split())} documents.")
    print(f"Final vocabulary size: {len(encoder.vocab)}")
    
    print("\n==================================================")
    print("BPE VOCABULARY AND MERGES")
    print("==================================================")
    
    # Display some vocabulary info
    vocab_info = encoder.get_vocab_info()
    print("\nSample of final vocabulary (Token ID -> Bytes):")
    for i in range(min(10, len(vocab_info))):
        token_id = sorted(vocab_info.keys())[i]
        print(f"  {token_id}: {vocab_info[token_id]} ({CustomUTF8Codec.decode(list(vocab_info[token_id]))})")
    
    # Display some merge info
    merges_info = encoder.get_merges_info()
    print("\nSample of learned merges (Pair -> New Token ID):")
    for i, (pair, new_id) in enumerate(merges_info.items()):
        if i >= 10: break
        print(f"  {pair} -> {new_id}")

    # Test encoding and decoding
    test_text = "Hello world wide web, café résumé, 123 banana."
    print(f"\n--- Testing encoding/decoding with: '{test_text}' ---")
    
    encoded_tokens = encoder.encode(test_text)
    decoded_text = encoder.decode(encoded_tokens)
    
    print(f"Original text: '{test_text}'")
    print(f"Encoded tokens: {encoded_tokens}")
    print(f"Decoded text: '{decoded_text}'")
    
    assert test_text == decoded_text, "Encoded and decoded text do not match!"
    print("✓ Encoding and decoding round-trip successful!")
    return encoder

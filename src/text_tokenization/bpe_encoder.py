#!/usr/bin/env python3
"""
Step 4.5: BPE Core Logic
For complete understanding of BPE at the byte level
"""

import sys
from typing import List, Tuple, Dict
from collections import defaultdict

from src.text_encoding.utf8_codec import CustomUTF8Codec

class CustomBPEEncoder:
    """
    BPE encoder using our custom UTF-8 functions
    """
    
    def __init__(self, normalizer):
        self.normalizer = normalizer
        self.vocab: Dict[bytes, int] = {} # Maps byte sequences to token IDs
        self.merges: Dict[Tuple[int, int], int] = {} # Maps (token_id1, token_id2) to new_token_id
        self.inverse_merges: Dict[int, Tuple[int, int]] = {} # Maps new_token_id to (token_id1, token_id2)
        self.token_to_bytes: Dict[int, bytes] = {} # Maps token IDs back to byte sequences
        self.next_token_id = 0
        
        self._build_initial_vocab()
    
    def _build_initial_vocab(self):
        """Build initial vocabulary of 256 bytes + special tokens"""
        
        # Special tokens
        special_tokens = {
            b'<|endoftext|>': self.next_token_id,
            b'<|unk|>': self.next_token_id + 1,
        }
        self.next_token_id += len(special_tokens)
        
        # Add special tokens
        for token_bytes, token_id in special_tokens.items():
            self.vocab[token_bytes] = token_id
            self.token_to_bytes[token_id] = token_bytes
        
        # Add all 256 byte tokens
        for byte_val in range(256):
            byte_seq = bytes([byte_val])
            self.vocab[byte_seq] = self.next_token_id
            self.token_to_bytes[self.next_token_id] = byte_seq
            self.next_token_id += 1
        
        print(f"Initial vocabulary size: {len(self.vocab)}")
    
    def _get_byte_pairs(self, tokens: List[int]) -> Dict[Tuple[int, int], int]:
        """Count frequency of consecutive byte pairs in a list of tokens."""
        pairs = defaultdict(int)
        for i in range(len(tokens) - 1):
            pairs[(tokens[i], tokens[i+1])] += 1
        return pairs

    def train(self, text_corpus: List[str], vocab_size: int):
        """
        Trains the BPE encoder on a given text corpus to build the vocabulary.
        """
        if vocab_size <= len(self.vocab):
            print(f"Warning: Requested vocab_size ({vocab_size}) is not larger than initial vocab ({len(self.vocab)}). No merges will be performed.")
            return

        print(f"Starting BPE training with target vocab size: {vocab_size}")
        
        # 1. Pre-tokenize the corpus into initial byte tokens
        # Each document in the corpus is a list of byte token IDs
        tokenized_corpus: List[List[int]] = []
        for text in text_corpus:
            normalized_text = self.normalizer.normalize(text)
            bytes_list = CustomUTF8Codec.encode(normalized_text)
            
            # Convert bytes to initial token IDs
            initial_tokens = [self.vocab[bytes([b])] for b in bytes_list]
            tokenized_corpus.append(initial_tokens)
        
        print(f"Corpus pre-tokenized into {len(tokenized_corpus)} documents.")

        # 2. Iteratively find and merge the most frequent pairs
        while len(self.vocab) < vocab_size:
            # Find the most frequent pair across the entire corpus
            all_pairs = defaultdict(int)
            for doc_tokens in tokenized_corpus:
                pairs_in_doc = self._get_byte_pairs(doc_tokens)
                for pair, count in pairs_in_doc.items():
                    all_pairs[pair] += count
            
            if not all_pairs:
                print("No more pairs to merge. Stopping training.")
                break
            
            # Get the most frequent pair
            best_pair = max(all_pairs, key=all_pairs.get)
            
            # Create a new token for this pair
            new_token_id = self.next_token_id
            self.next_token_id += 1
            
            # Get the byte sequence for the new token
            token1_bytes = self.token_to_bytes[best_pair[0]]
            token2_bytes = self.token_to_bytes[best_pair[1]]
            new_token_bytes = token1_bytes + token2_bytes
            
            self.vocab[new_token_bytes] = new_token_id
            self.token_to_bytes[new_token_id] = new_token_bytes
            self.merges[best_pair] = new_token_id
            self.inverse_merges[new_token_id] = best_pair
            
            print(f"Merge {len(self.merges)}: {best_pair} -> {new_token_id} (bytes: {new_token_bytes}) (Freq: {all_pairs[best_pair]})")
            
            # Apply the merge to the tokenized corpus
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
            
            if len(self.vocab) % 100 == 0:
                print(f"Current vocab size: {len(self.vocab)}")
        
        print(f"BPE training complete. Final vocab size: {len(self.vocab)}")
        print(f"Total merges learned: {len(self.merges)}")

    def encode(self, text: str) -> List[int]:
        """
        Encodes a text string into a list of BPE token IDs.
        """
        normalized_text = self.normalizer.normalize(text)
        bytes_list = CustomUTF8Codec.encode(normalized_text)
        
        # Convert bytes to initial token IDs
        tokens = [self.vocab[bytes([b])] for b in bytes_list]
        
        # Apply merges iteratively
        while True:
            # Find the best pair to merge in the current token sequence
            current_pairs = self._get_byte_pairs(tokens)
            
            best_pair_to_merge = None
            for pair, new_token_id in self.merges.items():
                if pair in current_pairs:
                    # Prioritize merges that were learned earlier (smaller new_token_id)
                    # This ensures deterministic encoding if multiple pairs have same frequency
                    if best_pair_to_merge is None or self.merges[best_pair_to_merge] > new_token_id:
                        best_pair_to_merge = pair
            
            if best_pair_to_merge is None:
                break # No more merges possible
            
            # Perform the merge
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

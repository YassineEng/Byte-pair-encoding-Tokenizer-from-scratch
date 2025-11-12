#!/usr/bin/env python3
"""
Step 11: Main Demonstration Script
Orchestrates the execution and testing of all previous steps.
"""

import time
from typing import Optional

# Import core modules
from src.step_06_normalizer import create_normalizer, UnicodeNormalizer
from src.step_04_database_builder import build_database
from src.step_05_lookup import UnicodeDatabaseWithIndex # For type hinting

# Import analysis and testing tools for each step
from src.analysis_tools.test_step_01_download_data import test_download_data
from src.analysis_tools.test_step_02_parse_data import test_parse_data
from src.analysis_tools.test_step_03_indexing import test_indexing_system
from src.analysis_tools.test_step_04_database_builder import test_database_builder
from src.analysis_tools.test_step_05_lookup import test_lookup_functions
from src.analysis_tools.test_step_06_normalizer import test_normalization_functions
from src.analysis_tools.test_step_07_utf8_codec import demonstrate_custom_utf8, compare_with_python_builtin
from src.analysis_tools.test_step_08_build_vocab import test_build_initial_vocab
from src.analysis_tools.test_step_09_get_pairs import test_get_byte_pairs
from src.analysis_tools.test_step_10_bpe_encoder import demonstrate_bpe

def main():
    """
    Main function to run all steps and their corresponding tests/demonstrations.
    """
    print("=" * 80)
    print("UNICODE BYTE PAIR ENCODER BUILD FROM SCRATCH - FULL DEMONSTRATION")
    print("=" * 80)

    overall_start_time = time.perf_counter()

    # Initialize shared resources
    database: Optional[UnicodeDatabaseWithIndex] = None
    normalizer: Optional[UnicodeNormalizer] = None

    # --- Step 01: Download Data ---
    step_start_time = time.perf_counter()
    test_download_data()
    print(f"Step 01 completed in {time.perf_counter() - step_start_time:.2f} seconds.\n")

    # --- Step 02: Parse Data ---
    step_start_time = time.perf_counter()
    test_parse_data()
    print(f"Step 02 completed in {time.perf_counter() - step_start_time:.2f} seconds.\n")

    # --- Initialize Database (once for all subsequent steps) ---
    print("\n" + "=" * 60)
    print("INITIALIZING SHARED UNICODE DATABASE")
    print("=" * 60)
    init_start_time = time.perf_counter()
    try:
        database = build_database()
        print("✓ Unicode Database initialized successfully.")
    except Exception as e:
        print(f"Error initializing Unicode Database: {e}")
        print("Exiting demonstration.")
        return
    print(f"Database initialization completed in {time.perf_counter() - init_start_time:.2f} seconds.\n")

    # --- Initialize Normalizer (once for all subsequent steps) ---
    print("\n" + "=" * 60)
    print("INITIALIZING SHARED UNICODE NORMALIZER")
    print("=" * 60)
    init_start_time = time.perf_counter()
    try:
        normalizer = create_normalizer()
        print("✓ Unicode Normalizer initialized successfully.")
    except Exception as e:
        print(f"Error initializing Unicode Normalizer: {e}")
        print("Falling back to a simple pass-through normalizer for BPE.")
        class SimpleNormalizer:
            def normalize(self, text):
                return text
        normalizer = SimpleNormalizer()
    print(f"Normalizer initialization completed in {time.perf_counter() - init_start_time:.2f} seconds.\n")


    # --- Step 03: Indexing System (and Performance Analysis) ---
    step_start_time = time.perf_counter()
    # test_indexing_system now expects the database object
    test_indexing_system(database)
    print(f"Step 03 completed in {time.perf_counter() - step_start_time:.2f} seconds.\n")

    # --- Step 04: Database Builder (and Caching) ---
    # This step's test function already handles building/caching internally
    # We can skip calling it again if the database is already built and passed
    # For now, we'll keep it as is, but it will use the cache.
    step_start_time = time.perf_counter()
    test_database_builder()
    print(f"Step 04 completed in {time.perf_counter() - step_start_time:.2f} seconds.\n")

    # --- Step 05: Lookup Functions ---
    step_start_time = time.perf_counter()
    # test_lookup_functions now expects the database object
    test_lookup_functions(database)
    print(f"Step 05 completed in {time.perf_counter() - step_start_time:.2f} seconds.\n")

    # --- Step 06: Normalization Functions ---
    step_start_time = time.perf_counter()
    # test_normalization_functions now expects the normalizer object
    test_normalization_functions(normalizer)
    print(f"Step 06 completed in {time.perf_counter() - step_start_time:.2f} seconds.\n")

    # --- Step 07: Custom UTF-8 Codec ---
    step_start_time = time.perf_counter()
    print("\n" + "=" * 60)
    print("STEP 07: CUSTOM UTF-8 ENCODER/DECODER")
    print("=" * 60)
    demonstrate_custom_utf8()
    compare_with_python_builtin()
    print(f"Step 07 completed in {time.perf_counter() - step_start_time:.2f} seconds.\n")

    # --- Step 08: Build Initial BPE Vocabulary ---
    step_start_time = time.perf_counter()
    test_build_initial_vocab()
    print(f"Step 08 completed in {time.perf_counter() - step_start_time:.2f} seconds.\n")

    # --- Step 09: Get Byte Pairs ---
    step_start_time = time.perf_counter()
    test_get_byte_pairs()
    print(f"Step 09 completed in {time.perf_counter() - step_start_time:.2f} seconds.\n")

    # --- Step 10: BPE Encoder Core Logic ---
    step_start_time = time.perf_counter()
    print("\n" + "=" * 60)
    print("STEP 10: BPE ENCODER CORE LOGIC")
    print("=" * 60)
    try:
        demonstrate_bpe(normalizer)
    except Exception as e:
        print(f"Error during BPE demonstration: {e}")
    print(f"Step 10 completed in {time.perf_counter() - step_start_time:.2f} seconds.\n")

    overall_end_time = time.perf_counter()
    print("\n" + "=" * 80)
    print(f"ALL STEPS AND DEMONSTRATIONS COMPLETED! Total time: {overall_end_time - overall_start_time:.2f} seconds.")
    print("=" * 80)

if __name__ == "__main__":
    main()
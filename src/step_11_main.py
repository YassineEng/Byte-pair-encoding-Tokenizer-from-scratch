#!/usr/bin/env python3
"""
Step 11: Main Demonstration Script
Orchestrates the execution and testing of all previous steps.
"""

# Import core modules
from src.step_06_normalizer import create_normalizer

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
from src.analysis_tools.analyze_random_unicode_data import main as analyze_random_unicode_data_main # Updated import

def main():
    """
    Main function to run all steps and their corresponding tests/demonstrations.
    """
    print("=" * 80)
    print("UNICODE BYTE PAIR ENCODER BUILD FROM SCRATCH - FULL DEMONSTRATION")
    print("=" * 80)

    # --- Step 01: Download Data ---
    test_download_data()

    # --- Step 02: Parse Data ---
    test_parse_data()

    # --- Step 03: Indexing System (and Performance Analysis) ---
    test_indexing_system()

    # --- Step 04: Database Builder (and Caching) ---
    test_database_builder()

    # --- Step 05: Lookup Functions ---
    test_lookup_functions()

    # --- Step 06: Normalization Functions ---
    test_normalization_functions()

    # --- Step 07: Custom UTF-8 Codec ---
    print("\n" + "=" * 60)
    print("STEP 07: CUSTOM UTF-8 ENCODER/DECODER")
    print("=" * 60)
    demonstrate_custom_utf8()
    compare_with_python_builtin()

    # --- Step 08: Build Initial BPE Vocabulary ---
    test_build_initial_vocab()

    # --- Step 09: Get Byte Pairs ---
    test_get_byte_pairs()

    # --- Step 10: BPE Encoder Core Logic ---
    print("\n" + "=" * 60)
    print("STEP 10: BPE ENCODER CORE LOGIC")
    print("=" * 60)
    try:
        print("Initializing Unicode Normalizer for BPE demonstration...")
        normalizer = create_normalizer()
        print("Unicode Normalizer initialized.")
        demonstrate_bpe(normalizer)
    except Exception as e:
        print(f"Error during BPE demonstration: {e}")

    # --- Auxiliary Analysis Tools ---
    print("\n" + "=" * 60)
    print("AUXILIARY ANALYSIS: RANDOM UNICODE DATA DISPLAY")
    print("=" * 60)
    try:
        analyze_random_unicode_data_main() # Call the main function from the renamed script
    except Exception as e:
        print(f"Error during random character analysis: {e}")

    print("\n" + "=" * 80)
    print("ALL STEPS AND DEMONSTRATIONS COMPLETED!")
    print("=" * 80)

if __name__ == "__main__":
    main()

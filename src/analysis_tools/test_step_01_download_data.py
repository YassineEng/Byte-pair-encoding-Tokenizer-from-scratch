#!/usr/bin/env python3
"""
Analysis and testing script for step_01_download_data.py.
Verifies the functionality of downloading Unicode data.
"""

import os
from src.step_01_download_data import download_unicode_data
from src.config import UNICODE_VERSION

def test_download_data():
    """
    Tests the download_unicode_data function.
    """
    print("\n" + "=" * 50)
    print("TESTING STEP 01: DOWNLOAD UNICODE DATA")
    print("=" * 50)

    filename = f"UnicodeData-{UNICODE_VERSION}.txt"

    # Clean up previous download if it exists
    if os.path.exists(filename):
        print(f"Removing existing file: {filename}")
        os.remove(filename)

    print(f"Attempting to download UnicodeData.txt version {UNICODE_VERSION}...")
    try:
        downloaded_filename = download_unicode_data(UNICODE_VERSION)
        if downloaded_filename == filename and os.path.exists(filename):
            print(f"✓ Successfully downloaded {downloaded_filename}.")
            print(f"  File size: {os.path.getsize(filename)} bytes.")
            
            # Read first few lines to confirm content
            with open(filename, 'r', encoding='utf-8') as f:
                print("\nFirst 5 lines of downloaded file:")
                for i, line in enumerate(f):
                    print(f"  {line.strip()}")
                    if i >= 4:
                        break
            print("\n" + "=" * 50)
            print("STEP 01 TEST COMPLETED SUCCESSFULLY!")
            print("=" * 50)
        else:
            print("✗ Download failed or returned incorrect filename.")
            print("\n" + "=" * 50)
            print("STEP 01 TEST FAILED!")
            print("=" * 50)
    except Exception as e:
        print(f"✗ An error occurred during download: {e}")
        print("\n" + "=" * 50)
        print("STEP 01 TEST FAILED!")
        print("=" * 50)

if __name__ == "__main__":
    test_download_data()

#!/usr/bin/env python3
"""
A script to download, parse, analyze, and process Unicode data.
"""

from unicode_magic.download_parse import (
    download_unicode_data,
    parse_unicode_data,
    download_east_asian_widths,
    download_unicode_auxiliary_files,
    parse_blocks,
    parse_scripts,
    parse_prop_list,
)
from unicode_magic.double_indexing import main as double_indexing_main

def main():
    """Main function to orchestrate the Unicode data processing pipeline."""
    double_indexing_main()

if __name__ == "__main__":
    # Run the main pipeline
    main()


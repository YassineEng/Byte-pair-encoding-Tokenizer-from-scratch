#!/usr/bin/env python3
"""
Step 2: Build Property Databases - CORRECT VERSION
Replicating the actual Python unicodedata architecture
"""

import sys
from typing import Dict, List, Set, Any
from collections import defaultdict
import json
import os

# Import from our Step 1
from unicode_magic.download_parse import (
    UnicodeChar,
    download_unicode_data,
    parse_unicode_data,
    download_east_asian_widths,
    download_unicode_auxiliary_files,
    parse_blocks,
    parse_scripts,
    parse_prop_list,
)

class UnicodePropertyDatabase:
    """
    Represents the actual Python UCD (Unicode Character Database) class
    This is what gets created by makeunicodedata.py in real Python
    """
    
    def __init__(self, chars: Dict[int, UnicodeChar]):
        self.chars = chars
        self._build_property_maps()
    
    def _build_property_maps(self):
        """Build the actual property maps used by Python's unicodedata"""
        print("Building Unicode property maps...")
        
        # These are the ACTUAL maps used in Python's implementation
        self.category_map = {}           # code_point -> category
        self.bidirectional_map = {}      # code_point -> bidi class  
        self.combining_map = {}          # code_point -> combining class
        self.mirrored_map = {}           # code_point -> mirrored flag
        self.decimal_map = {}            # code_point -> decimal value
        self.digit_map = {}              # code_point -> digit value
        self.numeric_map = {}            # code_point -> numeric value
        self.decomposition_map = {}      # code_point -> decomposition
        self.name_map = {}               # code_point -> name
        
        # Build the actual lookup maps
        for code_point, char in self.chars.items():
            self.category_map[code_point] = char.category
            self.bidirectional_map[code_point] = char.bidirectional
            self.combining_map[code_point] = char.combining
            self.mirrored_map[code_point] = char.mirrored
            self.decimal_map[code_point] = char.decimal
            self.digit_map[code_point] = char.digit
            self.numeric_map[code_point] = char.numeric
            self.decomposition_map[code_point] = char.decomposition
            self.name_map[code_point] = char.name
        
        print(f"✓ Built property maps for {len(self.chars)} characters")
    
    def category(self, char: str) -> str:
        """Get category for a character - like unicodedata.category()"""
        code_point = ord(char)
        return self.category_map.get(code_point, 'Cn')  # Cn = Other, Not Assigned
    
    def bidirectional(self, char: str) -> str:
        """Get bidirectional class - like unicodedata.bidirectional()"""
        code_point = ord(char)
        return self.bidirectional_map.get(code_point, '')
    
    def combining(self, char: str) -> int:
        """Get combining class - like unicodedata.combining()"""
        code_point = ord(char)
        return self.combining_map.get(code_point, 0)
    
    def mirrored(self, char: str) -> int:
        """Get mirrored property - like unicodedata.mirrored()"""
        code_point = ord(char)
        return 1 if self.mirrored_map.get(code_point) == 'Y' else 0
    
    def decimal(self, char: str, default=None):
        """Get decimal value - like unicodedata.decimal()"""
        code_point = ord(char)
        value = self.decimal_map.get(code_point)
        if value is None:
            if default is None:
                raise ValueError("not a decimal")
            return default
        return value
    
    def digit(self, char: str, default=None):
        """Get digit value - like unicodedata.digit()"""
        code_point = ord(char)
        value = self.digit_map.get(code_point)
        if value is None:
            if default is None:
                raise ValueError("not a digit")
            return default
        return value
    
    def numeric(self, char: str, default=None):
        """Get numeric value - like unicodedata.numeric()"""
        code_point = ord(char)
        value = self.numeric_map.get(code_point)
        if value is None:
            if default is None:
                raise ValueError("not a numeric character")
            return default
        
        # Convert numeric string to float (like Python does)
        try:
            return float(value)
        except (ValueError, TypeError):
            if default is None:
                raise ValueError("not a numeric character")
            return default
    
    def name(self, char: str, default=None) -> str:
        """Get character name - like unicodedata.name()"""
        code_point = ord(char)
        name = self.name_map.get(code_point)
        if name is None or name == '':
            if default is None:
                raise ValueError("no such name")
            return default
        return name
    
    def decomposition(self, char: str) -> str:
        """Get decomposition - like unicodedata.decomposition()"""
        code_point = ord(char)
        return self.decomposition_map.get(code_point, '')

class UnicodeAnalyzer:
    """Analyzes the actual Unicode data properties"""
    
    def __init__(self, database: UnicodePropertyDatabase):
        self.db = database
    
    def generate_real_statistics(self) -> Dict:
        """Generate statistics based on ACTUAL Unicode data"""
        stats = {
            'total_chars': len(self.db.chars),
            'categories': defaultdict(int),
            'bidi_classes': defaultdict(int),
            'combining_classes': defaultdict(int),
            'decimal_chars': 0,
            'digit_chars': 0,
            'numeric_chars': 0,
            'mirrored_chars': 0,
            'named_chars': 0,
        }
        
        for code_point, char in self.db.chars.items():
            # Count categories
            stats['categories'][char.category] += 1
            
            # Count bidi classes
            stats['bidi_classes'][char.bidirectional] += 1
            
            # Count combining classes
            stats['combining_classes'][char.combining] += 1
            
            # Count special properties
            if char.decimal is not None:
                stats['decimal_chars'] += 1
            if char.digit is not None:
                stats['digit_chars'] += 1
            if char.numeric is not None and char.numeric != '':
                stats['numeric_chars'] += 1
            if char.mirrored == 'Y':
                stats['mirrored_chars'] += 1
            if char.name and char.name != '':
                stats['named_chars'] += 1
        
        return stats
    
    def print_statistics(self):
        """Print accurate statistics"""
        stats = self.generate_real_statistics()
        
        print("\n" + "="*60)
        print("UNICODE DATABASE STATISTICS")
        print("="*60)
        
        print(f"\n📊 BASIC COUNTS:")
        print(f"  Total characters:      {stats['total_chars']:>8,}")
        print(f"  Named characters:      {stats['named_chars']:>8,}")
        print(f"  Decimal digits:        {stats['decimal_chars']:>8,}")
        print(f"  Digits:                {stats['digit_chars']:>8,}")
        print(f"  Numeric characters:    {stats['numeric_chars']:>8,}")
        print(f"  Mirrored characters:   {stats['mirrored_chars']:>8,}")
        
        print(f"\n🏷️  CATEGORIES ({len(stats['categories'])} total):")
        for cat, count in sorted(stats['categories'].items(), key=lambda x: x[1], reverse=True)[:10]:
            pct = (count / stats['total_chars']) * 100
            print(f"  {cat}: {count:>8,} ({pct:5.1f}%)")
        
        print(f"\n🔄 BIDIRECTIONAL CLASSES ({len(stats['bidi_classes'])} total):")
        for bidi, count in sorted(stats['bidi_classes'].items(), key=lambda x: x[1], reverse=True)[:8]:
            pct = (count / stats['total_chars']) * 100
            print(f"  {bidi}: {count:>8,} ({pct:5.1f}%)")
        
        print(f"\n🎯 COMBINING CLASSES ({len(stats['combining_classes'])} total):")
        # Show non-zero combining classes
        non_zero = {k: v for k, v in stats['combining_classes'].items() if k != 0}
        for comb, count in sorted(non_zero.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"  Class {comb}: {count:>8,}")

def test_unicode_functions(database: UnicodePropertyDatabase):
    """Test that our functions work like Python's unicodedata"""
    print("\n" + "="*50)
    print("TESTING UNICODE FUNCTIONS")
    print("="*50)
    
    test_cases = [
        ('A', "LATIN CAPITAL LETTER A"),
        ('9', "DIGIT NINE"), 
        ('À', "LATIN CAPITAL LETTER A WITH GRAVE"),
        ('¼', "VULGAR FRACTION ONE QUARTER"),
    ]
    
    for char, expected_name in test_cases:
        print(f"\nTesting: '{char}' (U+{ord(char):04X})")
        try:
            print(f"  Name:       {database.name(char)}")
            print(f"  Category:   {database.category(char)}")
            print(f"  Decimal:    {database.decimal(char, 'N/A')}")
            print(f"  Digit:      {database.digit(char, 'N/A')}")
            print(f"  Numeric:    {database.numeric(char, 'N/A')}")
            print(f"  Bidi:       {database.bidirectional(char)}")
            print(f"  Combining:  {database.combining(char)}")
            print(f"  Mirrored:   {database.mirrored(char)}")
            print(f"  Decomp:     {database.decomposition(char)}")
        except ValueError as e:
            print(f"  Error: {e}")

import json
import os
from typing import Any

def analyze_property_database(database: UnicodePropertyDatabase) -> Dict[str, Any]:
    """
    Analyze the property databases and return a summary.
    """
    print("\nAnalyzing property database for summary...")
    
    # Collect unique values for each property
    unique_categories = set()
    unique_bidi_classes = set()
    unique_combining_classes = set()
    unique_mirrored_values = set()
    unique_blocks = set()
    unique_scripts = set()
    unique_properties = set() # For binary properties from PropList.txt

    for char in database.chars.values():
        unique_categories.add(char.category)
        unique_bidi_classes.add(char.bidirectional)
        unique_combining_classes.add(char.combining)
        unique_mirrored_values.add(char.mirrored)
        unique_blocks.add(char.block)
        unique_scripts.add(char.script)
        for prop in char.properties:
            unique_properties.add(prop)

    # Calculate unique combinations of key properties
    unique_combinations = set()
    for char in database.chars.values():
        combo = (
            char.category,
            char.bidirectional,
            char.combining,
            char.mirrored,
            char.block,
            char.script,
            tuple(sorted(char.properties)) # Ensure consistent order for hashing
        )
        unique_combinations.add(combo)

    analysis = {
        "total_characters": len(database.chars),
        "unique_categories": len(unique_categories),
        "unique_bidi_classes": len(unique_bidi_classes),
        "unique_combining_classes": len(unique_combining_classes),
        "unique_mirrored_values": len(unique_mirrored_values),
        "unique_blocks": len(unique_blocks),
        "unique_scripts": len(unique_scripts),
        "unique_binary_properties": len(unique_properties),
        "total_unique_property_combinations": len(unique_combinations),
    }
    
    print("✓ Property database analysis complete.")
    return analysis

def save_property_database_summary(analysis: Dict, output_dir: str = "outputs/properties") -> None:
    """
    Save the property database analysis summary to a JSON file.
    """
    os.makedirs(output_dir, exist_ok=True)
    analysis_file = os.path.join(output_dir, "property_analysis_summary.json")
    with open(analysis_file, 'w', encoding='utf-8') as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)
    print(f"✓ Saved property analysis summary to: {analysis_file}")

def main():
    """Main function for Step 2"""
    print("="*60)
    print("STEP 2: BUILD UNICODE PROPERTY DATABASE")
    print("Replicating Python's unicodedata module structure")
    print("="*60)
    
    # Get data from Step 1
    try:
        unicode_version = "17.0.0"
        filename = download_unicode_data(unicode_version)
        ea_width_mapping = download_east_asian_widths(unicode_version)
        
        aux_files = download_unicode_auxiliary_files(unicode_version)
        blocks = parse_blocks(aux_files["Blocks"])
        scripts = parse_scripts(aux_files["Scripts"])
        prop_list = parse_prop_list(aux_files["PropList"])
        
        chars = parse_unicode_data(filename, blocks, scripts, prop_list)
    except Exception as e:
        print(f"Error: Could not load data from Step 1: {e}")
        sys.exit(1)
    
    # Build the actual Unicode property database
    database = UnicodePropertyDatabase(chars)
    
    # Analyze the data
    analyzer = UnicodeAnalyzer(database)
    analyzer.print_statistics()
    
    # Test our implementation
    test_unicode_functions(database)
    
    return database

if __name__ == "__main__":
    database = main()
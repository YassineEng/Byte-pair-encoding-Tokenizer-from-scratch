import urllib.request
import urllib.error
import os
import sys
from collections import namedtuple
from typing import Dict, List, Optional

# Define the character data structure
UnicodeChar = namedtuple('UnicodeChar', [
    'code_point',      # int: Unicode code point (e.g., 0x00C0)
    'name',            # str: Character name
    'category',        # str: General category (e.g., 'Lu', 'Nd')
    'combining',       # int: Canonical combining class (0-255)
    'bidirectional',   # str: Bidirectional class (e.g., 'L', 'R')
    'decomposition',   # str: Decomposition mapping
    'decimal',         # Optional[int]: Decimal digit value
    'digit',           # Optional[int]: Digit value  
    'numeric',         # Optional[str]: Numeric value (as string)
    'mirrored',        # str: 'Y' or 'N' for bidirectional mirroring
    'unicode1_name',   # str: Unicode 1.0 name
    'iso_comment',     # str: ISO 10646 comment
    'uppercase',       # Optional[int]: Uppercase mapping
    'lowercase',       # Optional[int]: Lowercase mapping
    'titlecase',       # Optional[int]: Titlecase mapping
    'block',           # str: Unicode block name
    'script',          # str: Unicode script name
    'properties',      # List[str]: List of binary properties
])

def download_unicode_data(unicode_version: str = "17.0.0") -> str:
    """
    Download the latest UnicodeData.txt file from unicode.org
    Returns the local filename if successful
    """
    filename = f"UnicodeData-{unicode_version}.txt"
    
    # Check if file already exists
    if os.path.exists(filename):
        print(f"Using existing file: {filename}")
        return filename
    
    url = f"https://www.unicode.org/Public/{unicode_version}/ucd/UnicodeData.txt"
    
    print(f"Downloading UnicodeData.txt version {unicode_version}...")
    print(f"URL: {url}")
    
    try:
        # Download the file
        urllib.request.urlretrieve(url, filename)
        print(f"Successfully downloaded: {filename}")
        return filename
        
    except urllib.error.URLError as e:
        print(f"Error downloading Unicode data: {e}")
        print("Please check your internet connection and the Unicode version.")
        sys.exit(1)

def parse_unicode_data(filename: str, blocks: Dict[range, str], scripts: Dict[range, str], prop_list: Dict[int, List[str]]) -> Dict[int, UnicodeChar]:
    """
    Parse the UnicodeData.txt file and return a dictionary mapping
    code points to UnicodeChar objects
    """
    chars = {}
    line_count = 0
    assigned_chars = 0
    
    print(f"Parsing {filename}...")
    
    def get_property_for_cp(cp: int, prop_map: Dict[range, str], default: str) -> str:
        for r, val in prop_map.items():
            if cp in r:
                return val
        return default

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                line_count += 1
                
                # Skip empty lines and comments
                if not line or line.startswith('#'):
                    continue
                
                # Split into fields (should be exactly 15 fields)
                fields = line.split(';')
                if len(fields) != 15:
                    print(f"Warning: Line {line_num} has {len(fields)} fields (expected 15): {line}")
                    continue
                
                # Parse code point (field 0)
                try:
                    code_point = int(fields[0], 16)
                except ValueError as e:
                    print(f"Error parsing code point on line {line_num}: {fields[0]}")
                    continue
                
                # Parse numeric fields (with proper handling of empty values)
                try:
                    combining = int(fields[3]) if fields[3] else 0
                except ValueError:
                    combining = 0
                
                # Parse decimal, digit, numeric (fields 6, 7, 8)
                decimal = int(fields[6]) if fields[6] else None
                digit = int(fields[7]) if fields[7] else None
                numeric = fields[8] if fields[8] else None
                
                # Parse case mappings (fields 12, 13, 14)
                uppercase = int(fields[12], 16) if fields[12] else None
                lowercase = int(fields[13], 16) if fields[13] else None
                titlecase = int(fields[14], 16) if fields[14] else None

                # Get Block, Script, and Properties
                char_block = get_property_for_cp(code_point, blocks, "No_Block")
                char_script = get_property_for_cp(code_point, scripts, "Unknown")
                char_properties = prop_list.get(code_point, [])
                
                # Create UnicodeChar object
                char = UnicodeChar(
                    code_point=code_point,
                    name=fields[1],
                    category=fields[2],
                    combining=combining,
                    bidirectional=fields[4],
                    decomposition=fields[5],
                    decimal=decimal,
                    digit=digit,
                    numeric=numeric,
                    mirrored=fields[9],
                    unicode1_name=fields[10],
                    iso_comment=fields[11],
                    uppercase=uppercase,
                    lowercase=lowercase,
                    titlecase=titlecase,
                    block=char_block,
                    script=char_script,
                    properties=char_properties,
                )
                
                chars[code_point] = char
                assigned_chars += 1
                
                # Progress reporting for large files
                if assigned_chars % 1000 == 0:
                    print(f"  Processed {assigned_chars} characters...")
                    
    except FileNotFoundError:
        print(f"Error: File {filename} not found!")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file {filename}: {e}")
        sys.exit(1)
    
    print(f"Parsing complete:")
    print(f"  Total lines processed: {line_count}")
    print(f"  Assigned characters: {assigned_chars}")
    print(f"  Code point range: 0x{min(chars.keys()):04X} - 0x{max(chars.keys()):04X}")
    
    return chars

def download_east_asian_widths(unicode_version: str = "15.0.0") -> Dict[int, str]:
    """
    Download and parse EastAsianWidth.txt for proper width information.
    """
    filename = f"EastAsianWidth-{unicode_version}.txt"
    url = f"https://www.unicode.org/Public/{unicode_version}/ucd/EastAsianWidth.txt"
    
    ea_widths = {}
    
    try:
        import urllib.request
        if not os.path.exists(filename):
            urllib.request.urlretrieve(url, filename)
            print(f"  Downloaded {filename}")
        else:
            print(f"  Using existing file: {filename}")
    except Exception as e:
        print(f"  Warning: Could not download {filename}: {e}. Using defaults.")
        return {}
    
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            if ';' in line:
                range_part, width = line.split(';', 1)
                width = width.split('#')[0].strip()
                
                if '..' in range_part:
                    start_hex, end_hex = range_part.split('..')
                    start = int(start_hex, 16)
                    end = int(end_hex, 16)
                    for cp in range(start, end + 1):
                        ea_widths[cp] = width
                else:
                    cp = int(range_part, 16)
                    ea_widths[cp] = width
    
    return ea_widths


def download_unicode_auxiliary_files(unicode_version: str = "17.0.0") -> Dict[str, str]:
    """
    Download auxiliary Unicode data files (Blocks.txt, Scripts.txt, PropList.txt).
    Returns a dictionary of local filenames if successful.
    """
    files_to_download = {
        "Blocks": f"https://www.unicode.org/Public/{unicode_version}/ucd/Blocks.txt",
        "Scripts": f"https://www.unicode.org/Public/{unicode_version}/ucd/Scripts.txt",
        "PropList": f"https://www.unicode.org/Public/{unicode_version}/ucd/PropList.txt",
    }
    
    downloaded_files = {}
    
    print("Downloading auxiliary Unicode data files...")
    
    for name, url in files_to_download.items():
        filename = f"{name}-{unicode_version}.txt"
        if os.path.exists(filename):
            print(f"Using existing file: {filename}")
            downloaded_files[name] = filename
            continue
        
        print(f"Downloading {name}.txt version {unicode_version}...")
        print(f"URL: {url}")
        
        try:
            urllib.request.urlretrieve(url, filename)
            print(f"Successfully downloaded: {filename}")
            downloaded_files[name] = filename
        except urllib.error.URLError as e:
            print(f"Error downloading {name}.txt: {e}")
            print("Please check your internet connection and the Unicode version.")
            sys.exit(1)
            
    return downloaded_files

def parse_blocks(filename: str) -> Dict[range, str]:
    """
    Parse the Blocks.txt file and return a dictionary mapping
    code point ranges to block names.
    """
    blocks = {}
    print(f"Parsing {filename}...")
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            if ';' in line:
                range_part, block_name = line.split(';', 1)
                range_part = range_part.strip()
                block_name = block_name.strip()
                
                start_hex, end_hex = range_part.split('..')
                start = int(start_hex, 16)
                end = int(end_hex, 16)
                blocks[range(start, end + 1)] = block_name
                
    print(f"Parsing complete: Found {len(blocks)} blocks.")
    return blocks

def parse_scripts(filename: str) -> Dict[range, str]:
    """
    Parse the Scripts.txt file and return a dictionary mapping
    code point ranges to script names.
    """
    scripts = {}
    print(f"Parsing {filename}...")
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            if ';' in line:
                range_part, script_name = line.split(';', 1)
                range_part = range_part.strip()
                script_name = script_name.split('#')[0].strip()
                
                if '..' in range_part:
                    start_hex, end_hex = range_part.split('..')
                    start = int(start_hex, 16)
                    end = int(end_hex, 16)
                    scripts[range(start, end + 1)] = script_name
                else:
                    start = int(range_part, 16)
                    scripts[range(start, start + 1)] = script_name
                    
    print(f"Parsing complete: Found {len(scripts)} script ranges.")
    return scripts

def parse_prop_list(filename: str) -> Dict[int, List[str]]:
    """
    Parse the PropList.txt file and return a dictionary mapping
    code points to a list of properties.
    """
    prop_list = {}
    print(f"Parsing {filename}...")
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            if ';' in line:
                range_part, prop_name = line.split(';', 1)
                range_part = range_part.strip()
                prop_name = prop_name.split('#')[0].strip()
                
                if '..' in range_part:
                    start_hex, end_hex = range_part.split('..')
                    start = int(start_hex, 16)
                    end = int(end_hex, 16)
                    for cp in range(start, end + 1):
                        prop_list.setdefault(cp, []).append(prop_name)
                else:
                    cp = int(range_part, 16)
                    prop_list.setdefault(cp, []).append(prop_name)
                    
    print(f"Parsing complete: Found properties for {len(prop_list)} code points.")
    return prop_list

def save_parsed_data(chars: Dict[int, UnicodeChar], output_file: str = "parsed_data.py") -> None:
    """
    Save the parsed data to a Python file for debugging
    """
    print(f"\nSaving parsed data to {output_file}...")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Parsed Unicode Data\n")
        f.write("# Generated by Step 1 of makeunicodedata.py\n\n")
        f.write("from collections import namedtuple\n\n")
        f.write("UnicodeChar = namedtuple('UnicodeChar', [\n")
        f.write("    'code_point', 'name', 'category', 'combining', 'bidirectional',\n")
        f.write("    'decomposition', 'decimal', 'digit', 'numeric', 'mirrored',\n")
        f.write("    'unicode1_name', 'iso_comment', 'uppercase', 'lowercase', 'titlecase'\n")
        f.write("])\n\n")
        f.write("chars = {\n")
        
        # Write first 100 characters as sample
        for i, (cp, char) in enumerate(sorted(chars.items())):
            if i >= 100:  # Limit output for readability
                f.write("    # ... and more ...\n")
                break
            f.write(f"    0x{cp:04X}: UnicodeChar(\n")
            f.write(f"        code_point=0x{cp:04X},\n")
            f.write(f"        name='{char.name}',\n")
            f.write(f"        category='{char.category}',\n")
            f.write(f"        combining={char.combining},\n")
            f.write(f"        bidirectional='{char.bidirectional}',\n")
            f.write(f"        decomposition='{char.decomposition}',\n")
            f.write(f"        decimal={char.decimal},\n")
            f.write(f"        digit={char.decimal},\n")
            f.write(f"        numeric='{char.numeric}',\n")
            f.write(f"        mirrored='{char.mirrored}',\n")
            f.write(f"        unicode1_name='{char.unicode1_name}',\n")
            f.write(f"        iso_comment='{char.iso_comment}',\n")
            f.write(f"        uppercase={char.uppercase},\n")
            f.write(f"        lowercase={char.lowercase},\n")
            f.write(f"        titlecase={char.titlecase}\n")
            f.write(f"    ),\n")
        
        f.write("}")
    
    print(f"Saved {min(100, len(chars))} sample characters to {output_file}")

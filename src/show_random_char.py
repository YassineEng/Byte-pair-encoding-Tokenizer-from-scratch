import random
from src.data_preparation.step_02_parse_data import UnicodeChar
from src.unicode_database.step_03_database_builder import build_database

def main():
    """
    Selects a random character from the Unicode data and displays
    a detailed breakdown of its properties using the UnicodePropertyDatabase.
    """
    print("--- Initializing Unicode Property Database ---")
    try:
        database = build_database()
    except Exception as e:
        print(f"Error initializing Unicode Property Database: {e}")
        return

    all_code_points = list(database.chars.keys())
    if not all_code_points:
        print("Error: No Unicode characters found in the database.")
        return

    # Choose a random code point
    random_cp = random.choice(all_code_points)
    char_obj = database.chars[random_cp]
    
    # --- Print the formatted output ---
    print("\n" + "="*60)
    print("RANDOM UNICODE CHARACTER PARSING EXAMPLE")
    print("="*60)

    # Reconstruct the raw line for display purposes
    raw_line_parts = [
        f"{char_obj.code_point:04X}",
        char_obj.name,
        char_obj.category,
        str(char_obj.combining),
        char_obj.bidirectional,
        char_obj.decomposition if char_obj.decomposition else '',
        str(char_obj.decimal) if char_obj.decimal is not None else '',
        str(char_obj.digit) if char_obj.digit is not None else '',
        char_obj.numeric if char_obj.numeric is not None else '',
        char_obj.mirrored,
        char_obj.unicode1_name if char_obj.unicode1_name else '',
        char_obj.iso_comment if char_obj.iso_comment else '',
        f"{char_obj.uppercase:04X}" if char_obj.uppercase is not None else '',
        f"{char_obj.lowercase:04X}" if char_obj.lowercase is not None else '',
        f"{char_obj.titlecase:04X}" if char_obj.titlecase is not None else '',
    ]
    raw_line = ";".join(raw_line_parts)
    raw_fields = raw_line.split(';')

    print(f"\n# Character: '{chr(char_obj.code_point)}' (U+{char_obj.code_point:04X})")
    print(f"raw_line = \"{raw_line}\"")

    print(f"\n# After parsing (everything strings):")
    print(f"raw_fields = {raw_fields}")

    print(f"\n# After type conversion:")
    print("converted_char = UnicodeChar(")
    print(f"    code_point=0x{char_obj.code_point:04X},        # int: {char_obj.code_point} (from \"{raw_fields[0]}\")")
    
    name_comment = 'unchanged' if char_obj.name == raw_fields[1] else f"(from '{raw_fields[1]}')"
    print(f"    name=\"{char_obj.name}\",        # str: {name_comment}")
    
    category_comment = 'unchanged' if char_obj.category == raw_fields[2] else f"(from '{raw_fields[2]}')"
    print(f"    category=\"{char_obj.category}\",            # str: {category_comment}")
    
    print(f"    combining={char_obj.combining},              # int: {char_obj.combining} (from \"{raw_fields[3]}\")")
    
    bidirectional_comment = 'unchanged' if char_obj.bidirectional == raw_fields[4] else f"(from '{raw_fields[4]}')"
    print(f"    bidirectional=\"{char_obj.bidirectional}\",       # str: {bidirectional_comment}")
    
    decomposition_comment = 'unchanged' if char_obj.decomposition == raw_fields[5] else f"(from '{raw_fields[5]}')"
    print(f"    decomposition=\"{char_obj.decomposition}\",         # str: {decomposition_comment}")
    
    decimal_comment = f"int: {char_obj.decimal} (from \"{raw_fields[6]}\")" if char_obj.decimal is not None else f"int: None (from \"{raw_fields[6]}\")"
    print(f"    decimal={char_obj.decimal},                # {decimal_comment}")
    
    digit_comment = f"int: {char_obj.digit} (from \"{raw_fields[7]}\")" if char_obj.digit is not None else f"int: None (from \"{raw_fields[7]}\")"
    print(f"    digit={char_obj.digit},                  # {digit_comment}")
    
    numeric_comment = f"str: {'kept as string for float conversion later' if char_obj.numeric is not None else 'None'} (from '{raw_fields[8]}')"
    print(f"    numeric=\"{char_obj.numeric}\",              # {numeric_comment}")
    
    mirrored_comment = f"str: {'will become 0 in C struct' if char_obj.mirrored == 'N' else 'will become 1 in C struct'} (from '{raw_fields[9]}')"
    print(f"    mirrored=\"{char_obj.mirrored}\",             # {mirrored_comment}")
    
    unicode1_name_comment = 'unchanged' if char_obj.unicode1_name == raw_fields[10] else f"(from '{raw_fields[10]}')"
    print(f"    unicode1_name=\"{char_obj.unicode1_name}\",   # str: {unicode1_name_comment}")
    
    iso_comment_comment = 'unchanged' if char_obj.iso_comment == raw_fields[11] else f"(from '{raw_fields[11]}')"
    print(f"    iso_comment=\"{char_obj.iso_comment}\",     # str: {iso_comment_comment}")
    
    uppercase_val = f"0x{char_obj.uppercase:04X}" if char_obj.uppercase is not None else "None"
    uppercase_comment = f"int: {char_obj.uppercase} (from \"{raw_fields[12]}\")" if char_obj.uppercase is not None else f"int: None (from \"{raw_fields[12]}\")"
    print(f"    uppercase={uppercase_val},       # {uppercase_comment}")
    
    lowercase_val = f"0x{char_obj.lowercase:04X}" if char_obj.lowercase is not None else "None"
    lowercase_comment = f"int: {char_obj.lowercase} (from \"{raw_fields[13]}\")" if char_obj.lowercase is not None else f"int: None (from \"{raw_fields[13]}\")"
    print(f"    lowercase={lowercase_val},       # {lowercase_comment}")
    
    titlecase_val = f"0x{char_obj.titlecase:04X}" if char_obj.titlecase is not None else "None"
    titlecase_comment = f"int: {char_obj.titlecase} (from \"{raw_fields[14]}\")" if char_obj.titlecase is not None else f"int: None (from \"{raw_fields[14]}\")"
    print(f"    titlecase={titlecase_val}        # {titlecase_comment}")
    print(")")

    print("\n1. Character details from UnicodePropertyDatabase:")
    print(f"   Code Point: U+{char_obj.code_point:04X} ('{chr(char_obj.code_point)}')")
    print(f"   Name: {char_obj.name}")
    print(f"   Category: {char_obj.category}")
    print(f"   Bidirectional Class: {char_obj.bidirectional}")
    print(f"   Combining Class: {char_obj.combining}")
    print(f"   Mirrored: {char_obj.mirrored}")
    print(f"   Decimal Value: {char_obj.decimal}")
    print(f"   Digit Value: {char_obj.digit}")
    print(f"   Numeric Value: {char_obj.numeric}")
    print(f"   Decomposition: {char_obj.decomposition}")

    # 2. Demonstrate unicodedata-like functions
    print("\n2. Demonstrating unicodedata-like function calls:")
    char_str = chr(char_obj.code_point)
    try:
        print(f"   database.category('{char_str}'): {database.category(char_str)}")
        print(f"   database.bidirectional('{char_str}'): {database.bidirectional(char_str)}")
        print(f"   database.combining('{char_str}'): {database.combining(char_str)}")
        print(f"   database.mirrored('{char_str}'): {database.mirrored(char_str)}")
        print(f"   database.decimal('{char_str}', default='N/A'): {database.decimal(char_str, default='N/A')}")
        print(f"   database.digit('{char_str}', default='N/A'): {database.digit(char_str, default='N/A')}")
        print(f"   database.numeric('{char_str}', default='N/A'): {database.numeric(char_str, default='N/A')}")
        print(f"   database.name('{char_str}'): {database.name(char_str)}")
        print(f"   database.decomposition('{char_str}'): {database.decomposition(char_str)}")
    except ValueError as e:
        print(f"   Error during function demonstration: {e}")

    print("="*60)


if __name__ == "__main__":
    main()

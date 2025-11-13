# Unicode Byte Pair Encoder (BPE) from Scratch

This project is an educational journey to build a Unicode character property database and a Byte Pair Encoding (BPE) tokenizer from first principles in Python. It aims to replicate core functionalities found in Python's `unicodedata` module and modern tokenization libraries, providing a deep understanding of Unicode handling and text processing. To enhance performance in critical sections, a Rust-based parser is integrated using `PyO3`.

Each `step_XX_*.py` file represents a distinct stage in building this system, progressively adding complexity and functionality.

## Project Structure

```
.
├───.gitignore
├───.python-version
├───LICENSE
├───PropList-17.0.0.txt
├───pyproject.toml
├───README.md
├───requirements.txt
├───Scripts-17.0.0.txt
├───unicode_database.bin
├───outputs\
│   └───parsed_chars.bin
└───src\
    ├───config.py
    ├───step_01_download_data.py
    ├───step_02_parse_data.py
    ├───step_03_indexing.py
    ├───step_04_database_builder.py
    ├───step_05_lookup.py
    ├───step_06_normalizer.py
    ├───step_07_utf8_codec.py
    ├───step_08_build_vocab.py
    ├───step_09_get_pairs.py
    ├───step_10_bpe_encoder.py
    ├───step_11_main.py
    ├───rust_parser\
    │   ├───Cargo.toml
    │   └───src\
    │       └───lib.rs
    └───analysis_tools\
        ├───analyze_random_unicode_data.py
        ├───test_step_01_download_data.py
        ├───... (other test files)
        └───visualize_database.py
```

## Getting Started

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/Unicode.git
    cd Unicode
    ```
2.  **Set up a virtual environment (recommended):**
    ```bash
    python -m venv .venv
    # On Windows
    .venv\Scripts\activate
    # On macOS/Linux
    source .venv/bin/activate
    ```
3.  **Install dependencies and build Rust extension:**
    ```bash
    pip install -r requirements.txt
    # Build and install the Rust parser
    cd src/rust_parser
    maturin develop
    cd ../..
    ```
4.  **Run the main demonstration script:**
    ```bash
    python -m src.step_11_main
    ```
    This script will execute all steps, download necessary data, build the database, and demonstrate the BPE encoder.

## Core Modules and Functionality

Contains global configuration variables for the project, such as the target Unicode version and the BPE training corpus.

*   **`UNICODE_VERSION`**: A string specifying the Unicode version to be used (e.g., "17.0.0").
*   **`BPE_TRAINING_CORPUS`**: A multi-line string containing the text used to train the BPE encoder. This can be modified to experiment with different training data.

### Full Demonstration Output

This section provides a condensed view of the output when running `python -m src.step_11_main`, showcasing the successful execution and key results from each step.

```
================================================================================
UNICODE BYTE PAIR ENCODER BUILD FROM SCRATCH - FULL DEMONSTRATION
================================================================================

==================================================
TESTING STEP 01: DOWNLOAD UNICODE DATA
==================================================
Attempting to download UnicodeData.txt version 17.0.0 (will use existing if present)...
Using existing file: UnicodeData-17.0.0.txt
✓ Successfully downloaded UnicodeData-17.0.0.txt.
  File size: 2198209 bytes.
==================================================
STEP 01 TEST COMPLETED SUCCESSFULLY!
==================================================
Step 01 completed in 0.00 seconds.


--- Testing get_parsed_unicode_chars function ---
Using existing file: UnicodeData-17.0.0.txt
Loading parsed Unicode characters from cache: outputs/parsed_chars.bin
✓ Successfully parsed 795 characters.
  Code point range: U+0000 - U+FB4F
--- parse_unicode_data function tests passed! ---
Step 02 completed in 0.00 seconds.


============================================================
INITIALIZING SHARED UNICODE DATABASE
============================================================
Loading Unicode database from cache: unicode_database.bin
✓ Database loaded successfully.
✓ Unicode Database initialized successfully.
Database initialization completed in 0.00 seconds.


============================================================
INITIALIZING SHARED UNICODE NORMALIZER
============================================================
============================================================
STEP 3: UNICODE NORMALIZATION AND LOOKUP FUNCTIONS
Replicating unicodedata.normalize() and unicodedata.lookup()
============================================================
Building normalization engine...
Building decomposition tables...
✓ Decomposition mappings: 252
  - Canonical: 130
  - Compatibility: 122
Building composition tables...
✓ Composition pairs: 125
============================================================
STEP 3 COMPLETED SUCCESSFULLY!
✓ Implemented Unicode normalization (NFC, NFD, NFKC, NFKD)
✓ Ready for Unicode version support!
============================================================
✓ Unicode Normalizer initialized successfully.
Normalizer initialization completed in 0.00 seconds.


==================================================
TESTING STEP 03: UNICODE INDEXING SYSTEM
==================================================
Testing character retrieval via index:
  U+0041 ('A'): Found 'LATIN CAPITAL LETTER A'
  U+00E9 ('é'): Found 'LATIN SMALL LETTER E WITH ACUTE'
  U+20AC ('€'): Found 'EURO SIGN'
==================================================
STEP 03 TEST COMPLETED SUCCESSFULLY!
==================================================
Step 03 completed in 0.00 seconds.


==================================================
TESTING STEP 04: UNICODE DATABASE BUILDER
==================================================
Removing existing cache file: unicode_database.bin
--- First build (should build from scratch) ---
Cache file not found. Building database from scratch...
Building double-indexed Unicode database...
✓ Created 471 unique character records
✓ Index1 size: 272 entries
✓ Index2 size: 12288 entries
✓ Unique index2 blocks: 3
✓ Built double index: 272 index1 entries, 12288 index2 entries
Caching new database to: unicode_database.bin
✓ First database build successful.
  Database version: 17.0.0
  Total characters: 795
--- Second build (should load from cache) ---
Loading Unicode database from cache: unicode_database.bin
✓ Database loaded successfully.
✓ Second database build successful (should be from cache).
==================================================
STEP 04 TEST COMPLETED SUCCESSFULLY!
==================================================
Step 04 completed in 0.03 seconds.


==================================================
TESTING STEP 05: UNICODE LOOKUP FUNCTIONS
==================================================
--- Testing 'A' (U+0041) ---
  Name: Expected='LATIN CAPITAL LETTER A', Actual='LATIN CAPITAL LETTER A' {✓}
  Category: Expected='Lu', Actual='Lu' {✓}
--- Testing '½' (U+00BD) ---
  Name: Expected='VULGAR FRACTION ONE HALF', Actual='VULGAR FRACTION ONE HALF' {✓}
  Numeric: Expected='0.5', Actual='0.5' {✓}
  Decomp: Expected='<fraction> 0031 2044 0032', Actual='<fraction> 0031 2044 0032' {✓}
==================================================
STEP 05 TEST COMPLETED SUCCESSFULLY!
==================================================
Step 05 completed in 0.00 seconds.


==================================================
TESTING STEP 06: UNICODE NORMALIZATION FUNCTIONS
==================================================
--- Testing 'café' with form 'NFC' ---
  Input: 'café'
  Form: NFC
  Expected: 'café' (Code Points: ['U+0063', 'U+0061', 'U+0066', 'U+00E9'])
  Actual:   'café' (Code Points: ['U+0063', 'U+0061', 'U+0066', 'U+00E9'])
  ✓ Test Passed
--- Testing 'Ü' with form 'NFD' ---
  Input: 'Ü'
  Form: NFD
  Expected: 'Ü' (Code Points: ['U+0055', 'U+0308'])
  Actual:   'Ü' (Code Points: ['U+0055', 'U+0308'])
  ✓ Test Passed
==================================================
STEP 06 TEST COMPLETED SUCCESSFULLY!
==================================================
Step 06 completed in 0.01 seconds.


============================================================
STEP 07: CUSTOM UTF-8 ENCODER/DECODER
============================================================
CUSTOM UTF-8 ENCODER/DECODER TEST
==================================================
Text: 'Hello, world!'
  Custom bytes: [72, 101, 108, 108, 111, 44, 32, 119, 111, 114, 108, 100, 33]
  Custom decoded: 'Hello, world!'
  Round-trip works: True
==================================================
COMPARISON WITH PYTHON BUILT-IN
==================================================
'€':
  Our bytes:    [226, 130, 172]
  Python bytes: [226, 130, 172]
  Match: True
  Our decode: '€'
  Python decode: '€'
  Both work: True
Step 07 completed in 0.00 seconds.


==================================================
TESTING STEP 08: BUILD INITIAL BPE VOCABULARY
==================================================
✓ Initial vocabulary built successfully.
  Total vocabulary size: 258
  Expected size: 258
Sample of vocabulary (Token ID -> Bytes):
  0: b'<|endoftext|>' ('<|endoftext|>')
  1: b'<|unk|>' ('<|unk|>')
  2: b'\x00' ('')
==================================================
STEP 08 TEST COMPLETED SUCCESSFULLY!
==================================================
Step 08 completed in 0.00 seconds.


==================================================
TESTING STEP 09: GET BYTE PAIRS
==================================================
--- Testing with tokens: [1, 2, 3, 1, 2] ---
  Expected pairs: {(1, 2): 2, (2, 3): 1, (3, 1): 1}
  Actual pairs:   {(1, 2): 2, (2, 3): 1, (3, 1): 1}
  ✓ Test Passed
==================================================
STEP 09 TEST COMPLETED SUCCESSFULLY!
==================================================
Step 09 completed in 0.00 seconds.


============================================================
STEP 10: BPE ENCODER CORE LOGIC
============================================================
==================================================
BPE TRAINING AND ENCODING/DECODING DEMONSTRATION
==================================================
Training BPE on corpus of 15 documents with 200 merges...
Initial vocabulary size: 258
Starting BPE training with target number of merges: 200
Corpus pre-tokenized into 134 documents.
Merge 1: (103, 34) -> 258 (bytes: b'e ') (Freq: 244)
Merge 100: (116, 99) -> 357 (bytes: b'ra') (Freq: 9)
  Current merges: 100/200
Merge 200: (121, 106) -> 457 (bytes: b'wh') (Freq: 5)
  Current merges: 200/200
BPE training complete. Final vocab size: 458
Total merges learned: 200

================================================================================
ALL STEPS AND DEMONSTRATIONS COMPLETED! Total time: 0.36 seconds.
================================================================================
```

### `src/config.py`

Contains global configuration variables for the project, such as the target Unicode version and the BPE training corpus.

*   **`UNICODE_VERSION`**: A string specifying the Unicode version to be used (e.g., "17.0.0").
*   **`BPE_TRAINING_CORPUS`**: A multi-line string containing the text used to train the BPE encoder. This can be modified to experiment with different training data.

### `src/step_01_download_data.py`

Handles the downloading of the `UnicodeData.txt` file from the official Unicode website.

*   **`download_unicode_data(unicode_version: str = UNICODE_VERSION) -> str`**
    *   **Description**: Downloads the `UnicodeData.txt` file for a specified Unicode version. If the file already exists locally, it uses the existing copy.
    *   **Parameters**:
        *   `unicode_version` (str): The version of Unicode data to download. Defaults to `config.UNICODE_VERSION`.
    *   **Returns**: (str) The local filename of the downloaded data.
    *   **Example**:
        ```python
        from src.step_01_download_data import download_unicode_data
        filename = download_unicode_data("15.0.0")
        print(f"Downloaded data to: {filename}")
        ```

### `src/step_02_parse_data.py`

This module now leverages a **Rust-based parser** (implemented using `PyO3`) for significantly improved performance in parsing the raw `UnicodeData.txt` file. It processes the data into structured `UnicodeChar` objects, applying filters for a simplified dataset, and implements caching for parsed data to speed up subsequent runs.

*   **`UnicodeChar` (PyO3 class from Rust)**
    *   **Description**: A class (exposed from Rust via `PyO3`) representing a single Unicode character with its various properties (code point, name, category, combining class, bidirectional class, decomposition, numeric values, case mappings, etc.). This Rust implementation provides substantial performance benefits over a pure Python equivalent.
*   **`get_parsed_unicode_chars(filename: str, version: str) -> Dict[int, UnicodeChar]`**
    *   **Description**: Retrieves parsed Unicode characters. It first attempts to load them from a cache file (`outputs/parsed_chars.bin`). If the cache is not found or is outdated, it calls the Rust parser to process the `UnicodeData.txt` file and then caches the result.
    *   **Parameters**:
        *   `filename` (str): Path to the `UnicodeData.txt` file.
        *   `version` (str): The Unicode version associated with the data.
    *   **Returns**: (Dict[int, UnicodeChar]) A dictionary mapping Unicode code points (integers) to `UnicodeChar` objects.
*   **Example**:
    ```python
    from src.step_01_download_data import download_unicode_data
    from src.step_02_parse_data import get_parsed_unicode_chars # Note: parse_unicode_data is now internal to Rust
    from src.config import UNICODE_VERSION

    data_file = download_unicode_data(UNICODE_VERSION)
    parsed_chars = get_parsed_unicode_chars(data_file, UNICODE_VERSION)
    print(f"Parsed {len(parsed_chars)} Unicode characters using Rust parser.")
    # Example: Get data for 'A' (U+0041)
    char_A = parsed_chars.get(0x41)
    if char_A:
        print(f"Name of U+0041: {char_A.name}")
    ```

### `src/step_03_indexing.py`

Implements a two-level indexing system (`index1` and `index2`) for efficient `O(1)` lookup of Unicode character properties, mirroring the approach used in Python's C implementation of `unicodedata`.

*   **`DoubleIndexedUnicodeDatabase` (class)**
    *   **Description**: A base class that sets up the double-indexing mechanism. It takes a dictionary of `UnicodeChar` objects and constructs `index1` and `index2` arrays to quickly locate character data.
    *   **`__init__(self, chars: Dict[int, UnicodeChar])`**: Initializes the database with parsed character data and builds the double index.
    *   **`_build_double_index(self)`**: Orchestrates the building of `index1` and `index2`.
    *   **`_build_character_records_index(self)`**: Maps unique character property signatures to record indices.
    *   **`_build_index_arrays(self, blocks)`**: Populates the `index1` and `index2` arrays.
    *   **`_get_record_index(self, code_point: int) -> int`**: Performs the double-indexed lookup to get the record index for a given code point.
    *   **`get_character_by_index(self, code_point: int) -> UnicodeChar`**: Retrieves the `UnicodeChar` object for a given code point using the underlying `chars` dictionary.
    *   **Example**: (Typically used via `UnicodeDatabaseWithIndex` in `step_05_lookup.py`)
        ```python
        # See step_04_database_builder.py for practical usage
        ```

### `src/step_04_database_builder.py`

Serves as the primary entry point for building and retrieving the complete Unicode database. It handles caching the `UnicodeDatabaseWithIndex` object to disk for persistence and faster loading.

*   **`build_database()`**
    *   **Description**: Constructs the `UnicodeDatabaseWithIndex`. It first attempts to load a cached version from `unicode_database.bin`. If the cache is missing or outdated (based on `UNICODE_VERSION`), it rebuilds the database from scratch by downloading and parsing data, then saves the new database to the cache.
    *   **Returns**: (`UnicodeDatabaseWithIndex`) An instance of the fully initialized Unicode database.
    *   **Example**:
        ```python
        from src.step_04_database_builder import build_database
        db = build_database()
        print(f"Database loaded/built for Unicode version: {db.version}")
        ```

### `src/step_05_lookup.py`

Extends the `DoubleIndexedUnicodeDatabase` to provide a comprehensive set of Unicode character property lookup functions, similar to those found in Python's `unicodedata` module.

*   **`UnicodeDatabaseWithIndex` (class)**
    *   **Description**: Inherits from `DoubleIndexedUnicodeDatabase` and adds methods for querying specific character properties.
    *   **`name(self, char_or_code_point: Union[str, int], default: Optional[str] = None) -> Optional[str]`**
        *   **Description**: Returns the official Unicode name of a character.
    *   **`category(self, char_or_code_point: Union[str, int]) -> str`**
        *   **Description**: Returns the general category of a character (e.g., 'Lu' for uppercase letter).
    *   **`decimal(self, char_or_code_point: Union[str, int], default: Optional[int] = None) -> Optional[int]`**
        *   **Description**: Returns the decimal value of a character if it represents a decimal digit.
    *   **`digit(self, char_or_code_point: Union[str, int], default: Optional[int] = None) -> Optional[int]`**
        *   **Description**: Returns the digit value of a character if it represents a digit.
    *   **`numeric(self, char_or_code_point: Union[str, int], default: Optional[float] = None) -> Optional[float]`**
        *   **Description**: Returns the numeric value of a character as a float (handles fractions).
    *   **`combining(self, char_or_code_point: Union[str, int]) -> int`**
        *   **Description**: Returns the canonical combining class of a character.
    *   **`bidirectional(self, char_or_code_point: Union[str, int]) -> str`**
        *   **Description**: Returns the bidirectional class of a character.
    *   **`mirrored(self, char_or_code_point: Union[str, int]) -> int`**
        *   **Description**: Returns 1 if the character is mirrored in bidirectional text, 0 otherwise.
    *   **`decomposition(self, char_or_code_point: Union[str, int]) -> str`**
        *   **Description**: Returns the decomposition mapping of a character.
    *   **`is_mirrored(self, char_or_code_point: Union[str, int]) -> bool`**
        *   **Description**: Convenience method to check if a character has the Bidi_Mirrored property.
    *   **`lookup(self, name: str) -> str`**
        *   **Description**: (Simplified) Looks up a character by its official Unicode name.
    *   **`normalize(self, form: str, text: str) -> str`**
        *   **Description**: (Placeholder) A placeholder for normalization functionality, which is fully implemented in `step_06_normalizer.py`.
    *   **Example**:
        ```python
        from src.step_04_database_builder import build_database
        db = build_database()

        char_euro = '€'
        print(f"Name of '{char_euro}': {db.name(char_euro)}")
        print(f"Category of '{char_euro}': {db.category(char_euro)}")

        char_half = '½'
        print(f"Numeric value of '{char_half}': {db.numeric(char_half)}")
        ```

### `src/step_06_normalizer.py`

Implements the core logic for Unicode normalization forms (NFC, NFD, NFKC, NFKD), including building decomposition and composition tables from the Unicode database.

*   **`UnicodeNormalizer` (class)**
    *   **Description**: A class that provides methods to normalize Unicode strings according to different normalization forms. It builds internal tables for decomposition and composition based on the `UnicodeDatabaseWithIndex`.
    *   **`__init__(self, database: UnicodeDatabaseWithIndex)`**: Initializes the normalizer with a Unicode database and builds internal decomposition/composition tables.
    *   **`_build_decomposition_tables(self)`**: Parses decomposition mappings from the Unicode data to create canonical and compatibility decomposition maps.
    *   **`_build_composition_tables(self)`**: Builds composition pairs for NFC/NFKC from canonical decomposition mappings.
    *   **`normalize(self, text: str, form: str = 'NFC') -> str`**
        *   **Description**: Normalizes a Unicode string `text` to the specified `form` (NFC, NFD, NFKC, NFKD).
        *   **Parameters**:
            *   `text` (str): The input Unicode string.
            *   `form` (str): The normalization form ('NFC', 'NFD', 'NFKC', 'NFKD').
        *   **Returns**: (str) The normalized string.
    *   **`_decompose(self, text: str, compatibility: bool = False) -> List[int]`**
        *   **Description**: Recursively decomposes a string into its constituent code points based on canonical or compatibility rules.
    *   **`_compose(self, code_points: List[int]) -> List[int]`**
        *   **Description**: Applies canonical composition to a list of decomposed code points.
    *   **`is_normalized(self, text: str, form: str = 'NFC') -> bool`**
        *   **Description**: Checks if a string is already in the specified normalization form.
    *   **`_quick_check(self, text: str, form: str) -> bool`**
        *   **Description**: A simplified quick check optimization for normalization.
*   **`create_normalizer()`**
    *   **Description**: A factory function that builds and returns a `UnicodeNormalizer` instance, ensuring the underlying Unicode database is properly initialized.
    *   **Returns**: (`UnicodeNormalizer`) An instance of the Unicode normalizer.
    *   **Example**:
        ```python
        from src.step_06_normalizer import create_normalizer
        normalizer = create_normalizer()

        text_nfd = "cafe\u0301" # e + combining acute accent
        text_nfc = "café"      # precomposed e with acute accent

        print(f"'{text_nfd}' in NFC: '{normalizer.normalize(text_nfd, 'NFC')}'")
        print(f"'{text_nfc}' in NFD: '{normalizer.normalize(text_nfc, 'NFD')}'")
        ```

### `src/step_07_utf8_codec.py`

Provides a custom implementation of a UTF-8 encoder and decoder, replicating the functionality of Python's built-in `str.encode('utf-8')` and `bytes.decode('utf-8')`.

*   **`CustomUTF8Codec` (class)**
    *   **Description**: A static class containing methods for encoding Unicode strings to UTF-8 byte sequences and decoding UTF-8 byte sequences back to Unicode strings.
    *   **`encode(text: str) -> List[int]` (static method)**
        *   **Description**: Encodes a Unicode string into a list of integers representing UTF-8 bytes.
        *   **Parameters**:
            *   `text` (str): The input Unicode string.
        *   **Returns**: (List[int]) A list of integers (0-255) representing the UTF-8 encoded bytes.
    *   **`_encode_code_point(code_point: int) -> List[int]` (static method)**
        *   **Description**: Encodes a single Unicode code point into its corresponding UTF-8 byte sequence.
    *   **`decode(bytes_list: List[int]) -> str` (static method)**
        *   **Description**: Decodes a list of integers (UTF-8 bytes) back into a Unicode string.
        *   **Parameters**:
            *   `bytes_list` (List[int]): A list of integers (0-255) representing UTF-8 bytes.
        *   **Returns**: (str) The decoded Unicode string.
    *   **Example**:
        ```python
        from src.step_07_utf8_codec import CustomUTF8Codec

        text = "Hello, world! café €"
        encoded_bytes = CustomUTF8Codec.encode(text)
        print(f"Encoded '{text}': {encoded_bytes}")

        decoded_text = CustomUTF8Codec.decode(encoded_bytes)
        print(f"Decoded bytes: '{decoded_text}'")
        ```

### `src/step_08_build_vocab.py`

A utility function to construct the initial vocabulary for the Byte Pair Encoding (BPE) tokenizer. This vocabulary includes all 256 possible byte values and special tokens.

*   **`build_initial_vocab() -> Tuple[Dict[bytes, int], Dict[int, bytes]]`**
    *   **Description**: Creates the foundational vocabulary for BPE. It maps single byte sequences (0-255) and special tokens (`<|endoftext|>`, `<|unk|>`) to unique integer token IDs, and vice-versa.
    *   **Returns**: (Tuple[Dict[bytes, int], Dict[int, bytes]]) A tuple containing:
        *   `vocab`: A dictionary mapping byte sequences (e.g., `b'a'`) to their integer token IDs.
        *   `token_to_bytes`: A dictionary mapping integer token IDs back to their byte sequences.
    *   **Example**:
        ```python
        from src.step_08_build_vocab import build_initial_vocab
        vocab, token_to_bytes = build_initial_vocab()
        print(f"Initial vocabulary size: {len(vocab)}")
        print(f"Token ID for 'a': {vocab[b'a']}")
        print(f"Bytes for token ID {vocab[b'a']}: {token_to_bytes[vocab[b'a']]}")
        ```

### `src/step_09_get_pairs.py`

A utility function used during BPE training to identify and count the frequency of consecutive byte pairs within a sequence of tokens.

*   **`get_byte_pairs(tokens: List[int]) -> Dict[Tuple[int, int], int]`**
    *   **Description**: Iterates through a list of token IDs and counts how many times each unique consecutive pair of tokens appears.
    *   **Parameters**:
        *   `tokens` (List[int]): A list of integer token IDs.
    *   **Returns**: (Dict[Tuple[int, int], int]) A dictionary where keys are `(token_id1, token_id2)` tuples and values are their frequencies.
    *   **Example**:
        ```python
        from src.step_09_get_pairs import get_byte_pairs
        token_sequence = [1, 2, 3, 1, 2, 4]
        pairs = get_byte_pairs(token_sequence)
        print(f"Byte pairs: {pairs}")
        # Expected: {(1, 2): 2, (2, 3): 1, (3, 1): 1, (2, 4): 1}
        ```

### `src/step_10_bpe_encoder.py`

Implements the core Byte Pair Encoding (BPE) algorithm. This class handles training a BPE model on a text corpus (now configurable via `src/config.py`), and then encoding and decoding text using the learned merges.

*   **`CustomBPEEncoder` (class)**
    *   **Description**: A BPE encoder that leverages the custom UTF-8 codec and Unicode normalizer. It learns merge rules by iteratively combining the most frequent byte pairs until a target vocabulary size is reached.
    *   **`__init__(self, normalizer)`**: Initializes the encoder with a Unicode normalizer and the initial byte-level vocabulary.
    *   **`train(self, num_merges: int)`**
        *   **Description**: Trains the BPE encoder on a text corpus (sourced from `config.BPE_TRAINING_CORPUS`). It normalizes the text, converts it to byte tokens, and then iteratively merges the most frequent byte pairs until `num_merges` have been performed.
        *   **Parameters**:
            *   `num_merges` (int): The number of merge operations to perform.
    *   **`encode(self, text: str) -> List[int]`**
        *   **Description**: Encodes a given text string into a sequence of BPE token IDs using the learned merge rules.
        *   **Parameters**:
            *   `text` (str): The input Unicode string to encode.
        *   **Returns**: (List[int]) A list of integer token IDs.
    *   **`decode(self, tokens: List[int]) -> str`**
        *   **Description**: Decodes a list of BPE token IDs back into a Unicode string.
        *   **Parameters**:
            *   `tokens` (List[int]): A list of integer token IDs.
        *   **Returns**: (str) The decoded Unicode string.
    *   **`get_vocab_info(self) -> Dict[int, bytes]`**
        *   **Description**: Returns the current vocabulary mapping token IDs to their byte representations.
    *   **`get_merges_info(self) -> Dict[Tuple[int, int], int]`**
        *   **Description**: Returns the learned merge rules, mapping a pair of token IDs to their merged token ID.
    *   **Example**:
        ```python
        from src.step_10_bpe_encoder import CustomBPEEncoder
        from src.step_06_normalizer import create_normalizer
        from src.config import BPE_NUM_MERGES # Import BPE_NUM_MERGES

        normalizer = create_normalizer()
        bpe_encoder = CustomBPEEncoder(normalizer)

        # The corpus is now read internally from config.BPE_TRAINING_CORPUS
        bpe_encoder.train(BPE_NUM_MERGES) # Pass only the number of merges

        text_to_encode = "hello world wide"
        encoded = bpe_encoder.encode(text_to_encode)
        decoded = bpe_encoder.decode(encoded)

        print(f"Original: '{text_to_encode}'")
        print(f"Encoded: {encoded}")
        print(f"Decoded: '{decoded}'")
        ```

### `src/step_11_main.py`

The main script that orchestrates the entire project. It runs through each step, demonstrating its functionality and integrating the components.

*   **`main()`**
    *   **Description**: Executes the full pipeline of the Unicode BPE encoder project. It calls the test and demonstration functions for each step (`step_01` through `step_10`), ensuring data downloading, parsing, database building, normalization, UTF-8 encoding/decoding, and BPE training/inference are all performed in sequence.
    *   **Example**: (This is the primary way to run the entire project demonstration.)
        ```bash
        python -m src.step_11_main
        ```

### `src/rust_parser/`

This directory contains the Rust project that provides a high-performance Unicode data parser, integrated into the Python project using `PyO3` and `maturin`.

*   **`src/rust_parser/src/lib.rs`**
    *   **Description**: Contains the core Rust logic for parsing `UnicodeData.txt`. It defines the `UnicodeChar` struct (exposed to Python via `#[pyclass]`) and the `parse_unicode_data` function (exposed via `#[pyfunction]`). This Rust implementation significantly speeds up the initial data parsing step.
*   **`src/rust_parser/Cargo.toml`**
    *   **Description**: The manifest file for the Rust project, defining its dependencies (e.g., `pyo3`) and metadata.

## Analysis Tools (`src/analysis_tools/`)

This directory contains scripts used for testing, analysis, and visualization of the different components of the Unicode project. Each `test_step_XX_*.py` file corresponds to a core step and verifies its functionality.

*   **`analyze_random_unicode_data.py`**: Selects a random Unicode character from the database and displays a detailed breakdown of its properties.
*   **`visualize_database.py`**: Loads the cached Unicode database and prints a human-readable visualization of its summary statistics, indexing system, and sample character records.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.

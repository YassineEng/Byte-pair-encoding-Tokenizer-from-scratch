import urllib.request
import urllib.error
import os
import sys

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

import requests
import time
import sys
import os

def download_file():
    # 1. Ask for the download link
    url = input("Enter the SVG download link: ").strip()
    
    # Simple filename extractor from URL
    filename = url.split("/")[-1] if "/" in url else "downloaded_file.svg"
    if not filename.endswith(".svg"):
        filename += ".svg"

    try:
        print(f"⏳ Downloading from {url}...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        with open(filename, 'wb') as f:
            f.write(response.content)
            
        # 2. Confirm download is complete
        print(f"✅ Download complete! Saved as: {filename}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

    # 3. Wait 3 seconds then auto close
    print("Program will close in 3 seconds...")
    time.sleep(3)
    sys.exit()

if __name__ == "__main__":
    download_file()

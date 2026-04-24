#!/usr/bin/env python3
"""
Download UDPipe Portuguese model properly
"""

import urllib.request
import os

def download_model():
    """Download the Portuguese UDPipe model"""

    # Try multiple sources
    urls = [
        # UD 2.10 model (older but reliable)
        "https://github.com/jwijffels/udpipe.models.ud.2.5/raw/master/inst/udpipe-ud-2.5-191206/portuguese-bosque-ud-2.5-191206.udpipe",
        # Alternative UD 2.5 model
        "https://lindat.mff.cuni.cz/repository/xmlui/bitstream/handle/11234/1-3131/portuguese-bosque-ud-2.5-191206.udpipe",
    ]

    output_file = "portuguese-bosque-ud.udpipe"

    for url in urls:
        try:
            print(f"Attempting download from: {url}")

            # Download with proper headers
            req = urllib.request.Request(
                url,
                headers={'User-Agent': 'Mozilla/5.0'}
            )

            with urllib.request.urlopen(req, timeout=60) as response:
                data = response.read()

                # Check if it's actually a model file (not HTML)
                if data.startswith(b'<'):
                    print("  Downloaded file is HTML, trying next source...")
                    continue

                # Save the file
                with open(output_file, 'wb') as f:
                    f.write(data)

                file_size = len(data) / (1024 * 1024)
                print(f"  Success! Downloaded {file_size:.2f} MB")
                print(f"  Saved as: {output_file}")
                return True

        except Exception as e:
            print(f"  Failed: {e}")
            continue

    print("\nAll download attempts failed.")
    print("Please manually download the model from:")
    print("https://lindat.mff.cuni.cz/repository/xmlui/handle/11234/1-3131")
    return False

if __name__ == "__main__":
    os.chdir("/Users/lucianadiasdemacedo/LEX-BR-Ius_extracao_data")
    download_model()

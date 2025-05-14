import pandas as pd
import requests
import io
import os
import time
import urllib.parse
import re

# 1. Dropbox shared link (must be shared with 'Anyone with the link')
dropbox_url = os.environ["INVOICING_BOOK_URL"]
if not dropbox_url:
    raise Exception("INVOICING_BOOK_URL is not set in the environment variables.")

# Extract file name from Dropbox URL
parsed_url = urllib.parse.urlparse(dropbox_url)
filename_match = re.search(r'/([^/?]+\.xlsb)', parsed_url.path)
if filename_match:
    base_filename = filename_match.group(1).replace('.xlsb', '.xlsx')
else:
    base_filename = "converted_output.xlsx"

# Log the start of the download
start_download_time = time.time()
print("Starting file download...")

# Download the file
response = requests.get(dropbox_url)
if response.status_code != 200:
    raise Exception("Failed to download file from Dropbox.")

download_time = time.time() - start_download_time
print(f"File downloaded in {download_time:.2f} seconds.")

# Convert the downloaded content to a binary stream
xlsb_file = io.BytesIO(response.content)

# Read the XLSB using pandas and pyxlsb
start_conversion_time = time.time()
print("Starting file conversion...")

excel_file = pd.ExcelFile(xlsb_file, engine='pyxlsb')
sheet_dict = excel_file.parse(sheet_name=None, header=None)

conversion_time = time.time() - start_conversion_time
print(f"Conversion completed in {conversion_time:.2f} seconds.")

# Write to XLSX
with pd.ExcelWriter(base_filename) as writer:
    for sheet_name, df in sheet_dict.items():
        df.to_excel(writer, sheet_name=sheet_name, index=False, header=False)

print(f"Conversion to XLSX completed. Output file: {base_filename}")

import pandas as pd
import requests
import io
import os
import time

# 1. Dropbox shared link (must be shared with 'Anyone with the link')
dropbox_url = os.environ["INVOICING_BOOK_URL"]

# 3. Download the file into memory
response = requests.get(dropbox_url)
if response.status_code != 200:
    raise Exception("Failed to download file from Dropbox.")

xlsb_file = io.BytesIO(response.content)

# 4. Read the XLSB using pandas and pyxlsb
excel_file = pd.ExcelFile(xlsb_file, engine='pyxlsb')
sheet_dict = excel_file.parse(sheet_name=None, header=None)

# 5. Write to XLSX
with pd.ExcelWriter("converted_output.xlsx") as writer:
    for sheet_name, df in sheet_dict.items():
        df.to_excel(writer, sheet_name=sheet_name, index=False, header=False)


# Log the start of the download
start_download_time = time.time()
print("Starting file download...")
response = requests.get(dropbox_url)
if response.status_code != 200:
    raise Exception("Failed to download file from Dropbox.")
download_time = time.time() - start_download_time
print(f"File downloaded in {download_time} seconds.")

# Proceed with file conversion...
start_conversion_time = time.time()
xlsb_file = io.BytesIO(response.content)
excel_file = pd.ExcelFile(xlsb_file, engine='pyxlsb')
sheet_dict = excel_file.parse(sheet_name=None, header=None)

# Log the completion of the conversion
conversion_time = time.time() - start_conversion_time
print(f"Conversion completed in {conversion_time} seconds.")

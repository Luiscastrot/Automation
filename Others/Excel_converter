import pandas as pd
import requests
import io
import os

# 1. Dropbox shared link (must be shared with 'Anyone with the link')
dropbox_url = os.environ["INVOICING_BOOK_URL"]

# 2. Convert to direct download link
direct_url = dropbox_url.replace('?dl=0', '?dl=1')

# 3. Download the file into memory
response = requests.get(direct_url)
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

import os
import requests
import io
import pandas as pd
import shutil

def convert_xlsb_to_xlsx(dropbox_url, target_folder):
    # Extract filename from URL
    filename = dropbox_url.split('/')[-1].split('?')[0]  # e.g. myfile.xlsb
    output_file = filename.replace('.xlsb', '.xlsx')

    # Download XLSB file from Dropbox
    r = requests.get(dropbox_url)
    r.raise_for_status()

    # Read XLSB file from bytes
    xlsb_data = io.BytesIO(r.content)
    xlsb = pd.ExcelFile(xlsb_data, engine='pyxlsb')

    # Write XLSX file locally
    with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
        for sheet in xlsb.sheet_names:
            df = xlsb.parse(sheet_name=sheet, header=None)
            df.to_excel(writer, sheet_name=sheet, index=False, header=False)

    # Move the converted file to the target folder if specified
    if target_folder:
        os.makedirs(target_folder, exist_ok=True)
        final_path = os.path.join(target_folder, output_file)
        shutil.move(output_file, final_path)
        output_file = final_path

    print(output_file)  # print filename or path for GitHub Actions

if __name__ == "__main__":
    dropbox_url = os.environ.get("INVOICING_BOOK_URL")
    target_folder = os.environ.get("TARGET_FOLDER", "")  # optional

    if not dropbox_url:
        raise Exception("INVOICING_BOOK_URL environment variable is missing")

    convert_xlsb_to_xlsx(dropbox_url, target_folder)

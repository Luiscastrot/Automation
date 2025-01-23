import requests
import base64
import csv
import logging
import os

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# API Credentials
api_username = "AlbertRogerUK"  # Replace with your Cin7 username
api_key = "d7fa15ce7fde46de82b53fd4dcaea663"  # Replace with your Cin7 API key

# API URL
BASE_URL = 'https://api.cin7.com/api/v1/SalesOrders'

def get_auth_header(username, key):
    credentials = f"{username}:{key}"
    encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
    return {'Authorization': f'Basic {encoded_credentials}', 'Content-Type': 'application/json'}

def call_api(url, headers):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json(), None
    except requests.RequestException as e:
        return None, str(e)

def process_sales_order(sales_order):
    # Flatten the sales order data
    flattened_data = {}
    for key, value in sales_order.items():
        if isinstance(value, dict):
            for sub_key, sub_value in value.items():
                flattened_data[f"{key}_{sub_key}"] = sub_value
        elif isinstance(value, list):
            for i, item in enumerate(value):
                for sub_key, sub_value in item.items():
                    flattened_data[f"{key}_{i+1}_{sub_key}"] = sub_value
        else:
            flattened_data[key] = value
    return flattened_data

def main():
    # Ask for the Sales Order ID
    sales_order_id = input("#FYB1131")
    
    headers = get_auth_header(api_username, api_key)
    url = f'{BASE_URL}/{sales_order_id}'
    
    logging.info(f"Fetching Sales Order {sales_order_id}...")
    
    data, error = call_api(url, headers)
    if error:
        logging.error(f"API call failed: {error}")
        return
    
    if data:
        processed_data = process_sales_order(data)
        
        # Generate CSV file name
        file_name = f"Sales_Order_{sales_order_id}.csv"
        
        # Write to CSV
        with open(file_name, mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=processed_data.keys())
            writer.writeheader()
            writer.writerow(processed_data)
        
        logging.info(f"Data successfully written to {file_name}")
        
        # Set environment variable for GitHub Actions
        env_file = os.getenv('GITHUB_ENV')
        if env_file:
            with open(env_file, "a") as env_file:
                env_file.write(f"ENV_CUSTOM_DATE_FILE={file_name}\n")
    else:
        logging.error(f"Sales Order {sales_order_id} not found.")

if __name__ == "__main__":
    main()

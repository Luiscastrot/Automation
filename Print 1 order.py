import requests
import base64
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# API Credentials
api_username = "AlbertRogerUK"  # Replace with your Cin7 username
api_key = "d7fa15ce7fde46de82b53fd4dcaea663"  # Replace with your Cin7 API key

# API URL
BASE_URL = 'https://api.cin7.com/api/v1'

def get_auth_header(username, key):
    credentials = f"{username}:{key}"
    encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
    return {
        'Authorization': f'Basic {encoded_credentials}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

def get_sales_order(order_id, headers):
    url = f'{BASE_URL}/PurchaseOrders//{order_id}'
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json(), None
    except requests.RequestException as e:
        return None, str(e)

def main():
    order_id = input("Enter the Sales Order ID: ")
    
    headers = get_auth_header(api_username, api_key)
    
    logging.info(f"Fetching Sales Order {order_id}...")
    
    data, error = get_sales_order(order_id, headers)
    if error:
        logging.error(f"API call failed: {error}")
        return
    
    if data:
        print(data)  # Print the JSON response
    else:
        logging.error(f"Sales Order {order_id} not found or an error occurred.")

if __name__ == "__main__":
    main()

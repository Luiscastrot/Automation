import requests
import base64

# API Credentials
api_username = "AlbertRogerUK"  # Replace with your Cin7 username
api_key = "d7fa15ce7fde46de82b53fd4dcaea663"  # Replace with your Cin7 API key

# Encode credentials for Basic Auth
credentials = f"{api_username}:{api_key}"
encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')

# API URL
BASE_URL = 'https://api.cin7.com/api/v1/Stock'

# Function to get stock movements
def get_stock_movements(page=1, rows_per_page=100):
    url = f'{BASE_URL}?page={page}&rows={rows_per_page}'
    headers = {
        'Authorization': f'Basic {encoded_credentials}',
        'Content-Type': 'application/json'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()  # Return JSON response if successful
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

def main():
    stock_movements = get_stock_movements()
    
    if stock_movements:
        # Print each stock movement as a single string
        for movement in stock_movements:
            print(str(movement))

if __name__ == "__main__":
    main()
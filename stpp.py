import requests
import json
import base64

# Take user input for API credentials and payout item ID
client_id = input("Enter PayPal client ID: ")
client_secret = input("Enter PayPal client secret: ")
payout_item_id = input("Enter payout item ID: ")

# Get access token with POST request to token endpoint
auth_string = f"{client_id}:{client_secret}"
auth_bytes = auth_string.encode('ascii')
auth_b64 = base64.b64encode(auth_bytes).decode('ascii')
headers = {
    'Authorization': f'Basic {auth_b64}',
    'Content-Type': 'application/x-www-form-urlencoded'
}
data = {
    'grant_type': 'client_credentials'
}
token_url = 'https://api.paypal.com/v1/oauth2/token'
response = requests.post(token_url, headers=headers, data=data)

# Save access token obtained from response
if 'access_token' in json.loads(response.text):
    access_token = json.loads(response.text)['access_token']
else:
    raise KeyError("Cannot find 'access_token' key in PayPal API response")

# Call Get Payout Item Details endpoint to check payment status
payout_item_url = f'https://api.paypal.com/v1/payments/payouts/{payout_item_id}'
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {access_token}'
}
response = requests.get(payout_item_url, headers=headers)

# Display payment status
payout_item_details = json.loads(response.text)
status = payout_item_details['batch_header']['batch_status']
print(f"Payment status: {status}")

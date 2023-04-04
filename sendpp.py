import requests
import json
import base64
import uuid

# Input kredensial API PayPal dan informasi transaksi dari pengguna
client_id = input("Masukkan client_id PayPal: ")
client_secret = input("Masukkan client_secret PayPal: ")
value = input("Masukkan nilai pembayaran: ")
note = input("Masukkan catatan pembayaran: ")
receiver = input("Masukkan email penerima: ")

# Mendapatkan token akses dengan permintaan POST ke endpoint token
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

# Menyimpan token akses yang diperoleh dari respons
if 'access_token' in json.loads(response.text):
    access_token = json.loads(response.text)['access_token']
else:
    raise KeyError("Tidak dapat menemukan kunci 'access_token' dalam respons API PayPal")

# Panggil endpoint Payouts untuk mengirimkan uang ke alamat email tertentu
payouts_url = 'https://api.paypal.com/v1/payments/payouts'
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {access_token}'
}
sender_batch_id = str(uuid.uuid4()) # menghasilkan sender_batch_id secara acak
sender_item_id = str(uuid.uuid4()) # menghasilkan sender_item_id secara acak
data = {
    'sender_batch_header': {
        'email_subject': 'Thanks',
        'sender_batch_id': sender_batch_id
    },
    'items': [
        {
            'recipient_type': 'EMAIL',
            'amount': {
                'value': value,
                'currency': 'USD'
            },
            'note': note,
            'sender_item_id': sender_item_id,
            'receiver': receiver
        }
    ]
}
response = requests.post(payouts_url, headers=headers, json=data)

# Menampilkan respons dari pengiriman uang
if response.status_code == 201:
    payout_item_id = json.loads(response.text)['batch_header']['payout_batch_id']
    print(f"Pembayaran sukses, payout_item_id: {payout_item_id}")
else:
    print(f"Pembayaran gagal, status code: {response.status_code}")
    print(f"Detail respons: {response.text}")

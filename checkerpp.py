import requests
from colorama import Fore, Style

# Inisialisasi colorama
Fore.GREEN, Fore.RED, Style.RESET_ALL  # Untuk kejelasan

# Baca kredensial dari file secret.txt
with open("secret.txt") as f:
    lines = f.read().splitlines()

for line in lines:
    try:
        client_id, client_secret = line.strip().split(":")
    except ValueError:
        print(f"{Fore.RED}Gak Valid client_id >> {line}{Style.RESET_ALL}")
        continue

    # Buat permintaan OAuth menggunakan kredensial tersebut
    url = "https://api.paypal.com/v1/oauth2/token"
    data = {"grant_type": "client_credentials"}

    response = requests.post(url, auth=(client_id, client_secret), data=data)

    # Parse dan simpan hasil yang valid dalam file validkey.txt
    if response.status_code == 200:
        result = response.json()
        access_token = result["access_token"]
        scope = result["scope"]
        app_id = result["app_id"]

        with open("validkey.txt", "a") as f:
            f.write(f"scope: {scope}\n")
            f.write(f"access_token: {access_token}\n")
            f.write(f"app_id: {app_id}\n")

        print(f"{Fore.GREEN}Valid client_id >> {client_id}{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Gak Valid client_id >> {client_id}{Style.RESET_ALL}")

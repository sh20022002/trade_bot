import requests

# Set up the base URL and headers for authentication
ip = os.getenv('SERVER_IP')
port = os.getenv('SERVER_PORT')
BASE_URL = f'{ip}:{port}'
HEADERS = {
    'Authorization': 'your_secure_token',
    'Content-Type': 'application/json'
}

def login(username, password):
    url = f"{BASE_URL}/login"
    data = {
        'username': username,
        'password': password
    }
    response = requests.post(url, json=data, verify='certs/server.crt.pem')
    if response.status_code == 200:
        print("Logged in successfully.")
        return response.json()
    else:
        print(f"Login failed: {response.json()}")
        return None

def logout():
    url = f"{BASE_URL}/logout"
    response = requests.post(url, headers=HEADERS, verify='certs/server.crt.pem')
    if response.status_code == 200:
        print("Logged out successfully.")
    else:
        print(f"Logout failed: {response.json()}")

def register(client_data):
    url = f"{BASE_URL}/register"
    response = requests.post(url, json=client_data, headers=HEADERS, verify='certs/server.crt.pem')
    if response.status_code == 200:
        print("Registration successful.")
        return response.json()
    else:
        print(f"Registration failed: {response.json()}")
        return None

def fetch_company_data():
    url = f"{BASE_URL}/fetch_company_data"
    response = requests.post(url, headers=HEADERS, verify='certs/server.crt.pem')
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch company data: {response.json()}")
        return None

def buy(symbol, amount):
    url = f"{BASE_URL}/buy"
    data = {
        'symbol': symbol,
        'amount': amount
    }
    response = requests.post(url, json=data, headers=HEADERS, verify='certs/server.crt.pem')
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to buy: {response.json()}")
        return None

def sell(symbol, amount):
    url = f"{BASE_URL}/sell"
    data = {
        'symbol': symbol,
        'amount': amount
    }
    response = requests.post(url, json=data, headers=HEADERS, verify='certs/server.crt.pem')
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to sell: {response.json()}")
        return None

def deposit(amount):
    url = f"{BASE_URL}/deposit"
    data = {
        'amount': amount
    }
    response = requests.post(url, json=data, headers=HEADERS, verify='certs/server.crt.pem')
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to deposit: {response.json()}")
        return None

def withdraw(amount):
    url = f"{BASE_URL}/withdraw"
    data = {
        'amount': amount
    }
    response = requests.post(url, json=data, headers=HEADERS, verify='certs/server.crt.pem')
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to withdraw: {response.json()}")
        return None




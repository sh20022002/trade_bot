import socket
import pickle
import threading, os

clients = {}

def handle_client(client_socket, client_id):
    while True:
        try:
            request = client_socket.recv(1024)
            if not request:
                break
            request_data = pickle.loads(request)
            command = request_data['command']
            data = request_data['data']
            
            if command == 'login':
                response = login(data)
            elif command == 'register':
                response = register(data)
            elif command == 'fetch_company_data':
                response = fetch_company_data(data)
            elif command == 'buy':
                response = buy(data)
            elif command == 'sell':
                response = sell(data)
            else:
                response = {'status': 'error', 'message': 'Invalid command'}
            
            client_socket.send(pickle.dumps(response))
        except Exception as e:
            print(f"Error handling client: {e}")
            break
    client_socket.close()
    del clients[client_id]

def login(data):
    # Implement your login logic here
    return {'status': 'success', 'message': 'Logged in'}

def register(data):
    # Implement your register logic here
    return {'status': 'success', 'message': 'Registered'}

def fetch_company_data(data):
    # Implement your fetch company data logic here
    return {'status': 'success', 'data': 'Company data'}

def buy(data):
    # Implement your buy logic here
    return {'status': 'success', 'message': 'Bought'}

def sell(data):
    # Implement your sell logic here
    return {'status': 'success', 'message': 'Sold'}

def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((os.getenv('IP'), os.getenv('PORT')))  
    server_socket.listen(5)
    print(f"Server listening on port {os.getenv('PORT')}...")

    while True:
        client_socket, addr = server_socket.accept()
        client_id = addr[1]
        print(f"Accepted connection from {addr} with client ID {client_id}")
        clients[client_id] = client_socket
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_id))
        client_handler.start()

if __name__ == "__main__":
    server()


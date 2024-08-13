import socket
import pickle
import threading, os, ssl
import database, main, client_handling

clients = {}

def handle_client(client_socket, client_id):
    """
    Handle the client requests and perform the corresponding actions based on the command received.

    Args:
        client_socket (socket.socket): The socket object representing the client connection.
        client_id (int): The ID of the client.

    Returns:
        None
    """
    try:
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
                elif command == 'deposit':
                    response = deposit(data)
                elif command == 'withdraw':
                    response = withdraw(data)
                else:
                    response = {'status': 'error', 'message': 'Invalid command'}
                
                client_socket.sendall(pickle.dumps(response))
            except Exception as e:
                print(f"Error handling client {client_id}: {e}")
                # Send error response back to client
                error_response = {'status': 'error', 'message': str(e)}
                try:
                    client_socket.sendall(pickle.dumps(error_response))
                except Exception as send_error:
                    print(f"Error sending error response to client {client_id}: {send_error}")
                break
    finally:
        client_socket.close()
        del clients[client_id]

def login(data):
    res = database.login(data['username'], data['password'])
    if res is None:
        return {'status': 'error', 'message': 'Invalid credentials'}
    companies = database.get_compenies()
    return {'status': 'success', 'message': 'Logged in', 'user': res, 'companies': companies}

def register(data):
    if client_handling.initialize(data):
        return {'status': 'success', 'message': 'Registered'}
    return {'status': 'error', 'message': 'Registration failed'}

def fetch_company_data(data):
    data = database.get_compenies()
    return {'status': 'success', 'data': data}

def buy(data):
    ans = client_handling.buy(data['symbol'], data['amount'])
    if ans != 'not sufficient cash in account!':
        return {'status': 'success', 'message': ans}
    return {'status': 'error', 'message': ans}

def sell(data):
    ans = client_handling.sell(data['symbol'], data['amount'])
    if ans != 'not sufficient cash in account!':
        return {'status': 'success', 'message': ans}
    return {'status': 'error', 'message': ans}

def deposit(data):
    ans = client_handling.deposit(data['amount'])
    return {'status': 'success', 'message': ans}

def withdraw(data):
    ans = client_handling.withdraw(data['amount'])
    if ans != 'not sufficient cash in account!':
        return {'status': 'success', 'message': ans}
    return {'status': 'error', 'message': ans}

def server():
    use_ssl = os.getenv('USE_SSL', 'False').lower() == 'true'

    if use_ssl:
        try:
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            context.load_cert_chain(certfile='certs/server.crt.pem', keyfile='certs/server.key.pem')
        except ssl.SSLError as e:
            print(f"SSL error: {e}")
            return
    
    ip = os.getenv('IP', '0.0.0.0')
    port = int(os.getenv('PORT', 3000))
    if not ip or port is None:
        raise ValueError("IP or Port is not set correctly")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((ip, port))  
        server_socket.listen(5)
        print(f'Listening on {ip}:{port}')
        
        if use_ssl:
            server_socket = context.wrap_socket(server_socket, server_side=True)

        while True:
            try:
                client, addr = server_socket.accept()
                client_id = addr[1]
                print(f"Accepted connection from {addr} with client ID {client_id}")
                clients[client_id] = client
                client_handler = threading.Thread(target=handle_client, args=(client, client_id))
                client_handler.start()
            except Exception as e:
                print(f"Error accepting connection: {e}")
                break

if __name__ == "__main__":
    server()

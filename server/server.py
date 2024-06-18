import socket
import pickle
import threading, os
import database, main

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
    security_socket = context.wrap_socket(client_socket, server_side=True)
    while True:
        try:
            request = security_socket.recv(1024)
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
        finally:
            security_socket.close()
            del clients[client_id]

def login(data):
    """
    Perform the login logic.

    Args:
        data (dict): The login data.

    Returns:
        dict: The login response.
    """
    # Implement your login logic here
    return {'status': 'success', 'message': 'Logged in',  'compenies': 'compenies'}

def register(data):
    """
    Perform the register logic.

    Args:
        data (dict): The register data.

    Returns:
        dict: The register response.
    """
    if database.add_client(data):
        return {'status': 'success', 'message': 'Registered'}

    return {'status': 'error', 'message': 'Registration failed'}


def fetch_company_data(data):
    """
    Fetch the company data.

    Args:
        data (dict): The data required for fetching company data.

    Returns:
        dict: The company data response.
    """
    data = database.get_compenies()

    return {'status': 'success', 'data': data}

def buy(data):
    """
    Perform the buy logic.

    Args:
        data (dict): The buy data.

    Returns:
        dict: The buy response.
    """
    # Implement your buy logic here
    return {'status': 'success', 'message': 'Bought'}

def sell(data):
    """
    Perform the sell logic.

    Args:
        data (dict): The sell data.

    Returns:
        dict: The sell response.
    """
    # Implement your sell logic here
    return {'status': 'success', 'message': 'Sold'}

def server():
    """
    Start the server and listen for client connections.
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((os.getenv('IP'), os.getenv('PORT')))  
    server_socket.listen(5)
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile='server.crt', keyfile='server.key')

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
    main.main()


import socket
import pickle
import threading, os, ssl
import database, main, client_handling


clients = {}

def handle_client(socket, client_id):
    """
    Handle the client requests and perform the corresponding actions based on the command received.

    Args:
        client_socket (socket.socket): The socket object representing the client connection.
        client_id (int): The ID of the client.

    Returns:
        None
    """
    
    

    while True:
        try:
            request = socket.recv(1024)
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
        
            socket.send(pickle.dumps(response))
        except Exception as e:
            print(f"Error handling client: {e}")
            break
        finally:
            socket.close()
            del clients[client_id]

def login(data):
    """
    Perform the login logic.

    Args:
        data (dict): The login data.

    Returns:
        dict: The login response.
    """
    
    res = database.login(data['username'], data['password'])
    if res == None:
        return {'status': 'error', 'message': 'Invalid credentials'}
    compenies = database.get_compenies()
    return {'status': 'success', 'message': 'Logged in', 'user': res,  'compenies': compenies }

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
    ans = client_handling.buy(data['symbol'], data['amount'])
    if ans != 'not sefichant cash in account!':
        return {'status': 'success', 'message': ans}
    return {'status': 'error', 'message': ans}

def sell(data):
    """
    Perform the sell logic.

    Args:
        data (dict): The sell data.

    Returns:
        dict: The sell response.
    """
    ans = client_handling.sell(data['symbol'], data['amount'])
    if ans != 'not sefichant cash in account!':
        return {'status': 'success', 'message': ans}
    return {'status': 'error', 'message': ans}

def deposit(data):
    """
    Perform the deposit logic.

    Args:
        data (dict): The deposit data.

    Returns:
        dict: The deposit response.
    """
    ans = client_handling.deposit(data['amount'])
    return {'status': 'success', 'message': ans}

def withdraw(data):
    """
    Perform the withdraw logic.

    Args:
        data (dict): The withdraw data.

    Returns:
        dict: The withdraw response.
    """
    ans = client_handling.withdraw(data['amount'])
    if ans != 'not sefichant cash in account!':
        return {'status': 'success', 'message': ans}
    else:
        return {'status': 'error', 'message': ans}

def server():
    """
    Start the server and listen for client connections.
    """
    use_ssl = True

    if use_ssl:
        try:
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            context.load_cert_chain(certfile='certs/server.crt.pem', keyfile='certs/server.key.pem')
            # context.check_hostname = False
        except ssl.SSLError as e:
            print(f"SSL error: {e}")
            return
    ip = os.getenv('IP', '0.0.0.0')
    port = os.getenv('PORT', '3000')
    if not ip or port is None:
        raise ValueError("IP or Port is not set correctly")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((ip, int(port)))  
        server_socket.listen(5)
        
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
                server_socket.close()
                break

if __name__ == "__main__":
    server()
    
    


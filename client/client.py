import time, os
import socket
import ssl
import pickle

def create_client_socket():
    """
    Creates a client socket.

    Returns:
        socket.socket: The client socket object.
        ssl.SSLContext: The SSL context if SSL is enabled, otherwise None.
    """
    use_ssl = os.getenv('USE_SSL', 'False').lower() == 'true'
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    if use_ssl:
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        cert_path = os.getenv('CERT_PATH', 'cert/server.crt.pem')
        context.load_verify_locations(cert_path)
        return client_socket, context
    
    return client_socket, None

def send_request(command, data):
    """
    Sends a request to the server and receives the response.

    Args:
        command (str): The command to send to the server.
        data (any): The data to send along with the command.

    Returns:
        any: The response received from the server.
    """
    client_socket, context = create_client_socket()
    server_ip = os.getenv('SERVER_IP', 'server')
    server_port = int(os.getenv('SERVER_PORT', '3000'))

    if not server_ip or server_port is None:
        raise ValueError("Server IP or Port is not set correctly")

    # Connect to the server
    client_socket.connect((server_ip, server_port))

    # Wrap the socket with SSL if SSL is enabled
    if context is not None:
        client_socket = context.wrap_socket(client_socket, server_hostname=os.getenv('SERVER_HOSTNAME', 'localhost'))

    # Send the request to the server
    request = {'command': command, 'data': data}
    client_socket.sendall(pickle.dumps(request))

    # Receive the response from the server
    response = client_socket.recv(4096)
    client_socket.close()

    if not response:
        raise EOFError("Received empty response from server")
    raise EOFError(f'{response}')
    
    return pickle.loads(response)

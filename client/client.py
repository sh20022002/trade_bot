
import streamlit as st
import time, os
import socket
import ssl
import pickle

def create_client_socket():
    """
    Creates a client socket.

    Args:
        port (int): The port number to connect to. Default is 9999.

    Returns:
        socket.socket: The client socket object.
    """

    use_ssl = True

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    if use_ssl:
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=os.getenv('CERT_PATH', 'cert/server.crt.pem'))
        # context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        # os.chdir(os.path.dirname(__file__))
        # context.load_verify_locations(os.getenv('CERT_PATH', 'cert/server.crt.pem'))
        # context.check_hostname = False

        # client_socket = ssl.wrap_socket(client_socket, ca_certs=os.getenv('CERT_PATH', 'cert/server.crt.pem'), ssl_version=ssl.PROTOCOL_TLSv1_2)
        # client_socket = context.wrap_socket(client_socket, server_hostname=os.getenv('SERVER_HOSTNAME', 'localhost'))

    
    return client_socket, context


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
    server_port = os.getenv('SERVER_PORT', '3000')

    if not server_ip or server_port is None:
        raise ValueError("Server IP or Port is not set correctly")
    
    
    # Now use server_ip and server_port in your connection logic
    client_socket.connect((server_ip, server_port))
    if context:
        client_socket = context.wrap_socket(client_socket, server_hostname=os.getenv('SERVER_HOSTNAME', 'localhost'))
    
    request = {'command': command, 'data': data}
    client_socket.sendall(pickle.dumps(request))
    
    response = client_socket.recv(4096)
    client_socket.close()
    
    return pickle.loads(response)

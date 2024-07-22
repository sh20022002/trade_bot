
import streamlit as st
import time
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
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.load_verify_locations('/ctrs/server.csr')
    client_socket = context.wrap_socket(client_socket, server_hostname=os.getenv('SERVER_IP'))
    return client_socket


def send_request(command, data):
    """
    Sends a request to the server and receives the response.

    Args:
        command (str): The command to send to the server.
        data (any): The data to send along with the command.

    Returns:
        any: The response received from the server.
    """
    client_socket = create_client_socket()
    client_socket.connect((os.getenv('SERVER_IP'), os.getenv('PORT')))
    
    request = {'command': command, 'data': data}
    client_socket.send(pickle.dumps(request))
    
    response = client_socket.recv(2048)
    client_socket.close()
    
    return pickle.loads(response)



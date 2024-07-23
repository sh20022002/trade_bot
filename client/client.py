
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
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    context = ssl.create_default_context()
    
    
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
    server_ip = os.getenv('SERVER_IP')
    server_port = os.getenv('SERVER_PORT', type=int)

    if not server_ip or server_port is None:
        raise ValueError("Server IP or Port is not set correctly")

    # Now use server_ip and server_port in your connection logic
    client_socket.connect((server_ip, int(server_port)))
    
    cert = client_socket.getpeercert()
    
    request = {'command': command, 'data': data}
    client_socket.send(pickle.dumps(request))
    
    response = client_socket.recv(2048)
    client_socket.close()
    
    return pickle.loads(response)



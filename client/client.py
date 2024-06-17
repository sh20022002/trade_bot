import server, database
import scraping
import streamlit as st
import time
import keyboard
import os
import psutil
import yfinance as yf
import pandas as pd

import socket
import ssl
import pickle

def create_client_socket( port=9999):
    host = os.gethostname()
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return client_socket

def send_object(client_socket, obj):
    try:
        data = pickle.dumps(obj)
        client_socket.send(data)

        response = client_socket.recv(1024) #mait need more than 1024 bytes
        response_obj = pickle.loads(response)
        print(f"Received response: {response_obj}")
    except Exception as e:
        print(f"Error sending object: {e}")
    finally:
        client_socket.close()

def start_client():
    client_socket = create_client_socket()
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    with context.wrap_socket(client_socket, server_hostname=os.getenv('SERVER_IP')) as tls_socket:
        tls_socket.connect((os.getenv('SERVER_IP'), 65432)) ###
        obj = {"message": "Hello, server!"}
        send_object(tls_socket, obj)

if __name__ == "__main__":
    start_client()


def send_request(command, data):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((os.getenv('SERVER_IP'), os.getenv('PORT')))
    
    request = {'command': command, 'data': data}
    client_socket.send(pickle.dumps(request))
    
    response = client_socket.recv(1024)
    client_socket.close()
    
    return pickle.loads(response)

# Example usage
if __name__ == "__main__":
    response = send_request('login', {'username': 'user', 'password': 'pass'})
    print(response)
    
    response = send_request('fetch_company_data', {'company': 'AAPL'})
    print(response)



stocks, compenies= initialize()


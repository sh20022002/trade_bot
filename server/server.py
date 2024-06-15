import socket
import ssl
import pickle, os

def create_server_socket(port=65432):
    host = os.gethostname()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    return server_socket

def handle_client(client_socket):
    try:
        data = client_socket.recv(1024)
        obj = pickle.loads(data)
        print(f"Received object: {obj}")

        # Send a response
        response = {"status": "success"}
        client_socket.send(pickle.dumps(response))
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        client_socket.close()

def start_server():
    server_socket = create_server_socket()
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile='server.crt', keyfile='server.key')

    with server_socket:
        while True:
            client_socket, addr = server_socket.accept()
            print(f"Connection from {addr}")
            with context.wrap_socket(client_socket, server_side=True) as tls_socket:
                handle_client(tls_socket)

if __name__ == "__main__":
    start_server()

import socket, os, threading


def start_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip = gethostbyname(gethostname())
    port = 8080
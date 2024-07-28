#!/bin/sh

# Get the server container's IP address
SERVER_IP=$(getent hosts server_container | awk '{ print $1 }')

# Export the IP address as an environment variable
export SERVER_IP=$SERVER_IP

# Run the client script
python client.py

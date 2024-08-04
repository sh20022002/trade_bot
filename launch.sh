#!/bin/bash

# Define the path for the certs directory
CERTS_DIR="certs"
# Create the certs directory with root permissions if it doesn't exist
mkdir -p "$CERTS_DIR"

# Generate the certificate signing request with root permissions
openssl req -new -newkey rsa:2048 -nodes -keyout "certs/server.key.pem" -out "certs/server.csr.pem"

# Generate the self-signed certificate with root permissions
openssl x509 -req -days 365 -in "certs/server.csr.pem" -signkey "certs/server.key.pem" -out "certs/server.crt.pem"

echo "Self-signed certificate generated in certs"

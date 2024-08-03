#!/bin/bash

# Define the path for the certs directory


# Create the certs directory with root permissions
mkdir -p certs

# Generate the self-signed certificate with root permissions
openssl genrsa -outform PEM -out "certs/server.key.pem" 2048
openssl req -new -x509 -days 365 -subj "/C=IL/ST=TelAviv/L=TelAviv/O=SmartTraid/OU=R\&D/CN=shmuel-xps/emailAddress=shmuel.tor@gmail.com" -key certs/server.key.pem -outform PEM -out certs/server.csr.pem
openssl x509 -req -days 365 -in "certs/server.csr.pem" -signkey "certs/server.key.pem" -outform PEM -out "certs/server.crt.pem"

echo "Self-signed certificate generated in certs"


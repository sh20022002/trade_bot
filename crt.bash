
# enshure that you are in the server directory
# and that you have the openssl installed
mkdir certs
openssl genrsa -out certs/server.key 2048
openssl req -new -key certs/server.key -out certs/server.crt
openssl x509 -signkey certs/server.key -in certs/server.crt -req -days 365 -out certs/certificate.crt

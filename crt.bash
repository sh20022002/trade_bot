
# enshure that you are in the server directory
# and that you have the openssl installed

openssl genrsa -out server.key 2048
openssl req -new -key server.key -out server.csr

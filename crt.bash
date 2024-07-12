
# enshure that you are in the server directory
# and that you have the openssl installed
mkdir crts
openssl genrsa -out crts/server.key 2048
openssl req -new -key crts/server.key -out crts/server.csr

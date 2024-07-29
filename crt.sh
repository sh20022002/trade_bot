# Desc: Generate a self-signed certificate for the server
mkdir -p certs
openssl genrsa -out certs/server.key.pem 2048
openssl req -new -key certs/server.key.pem -out certs/server.csr.pem "/C=US/ST=California/L=San Francisco/O=YourCompany/OU=YourDepartment/CN=$hostname/emailAddress=your_email@example.com"
openssl x509 -req -days 365 -in certs/server.csr.pem -signkey certs/server.key.pem -out certs/server.crt.pem

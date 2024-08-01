# Desc: Generate a self-signed certificate for the server
mkdir -p certs
openssl genrsa -out certs/server.key.pem 2048
openssl req -new -key certs/server.key.pem -out certs/server.csr.pem -subj "/C=is/ST=tel aviv/L=tel aviv/O=SmarTraid/OU=R&D/CN=$hostname/emailAddress=shmuel.tor@gmail.com"\n\
openssl x509 -req -days 365 -in certs/server.csr.pem -signkey certs/server.key.pem -out certs/server.crt.pem
# docker-compose up --build -d
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io
docker pull mongo
docker run --name mongodb -d -p 27017:27017 -v ~/mongo-data:/data/db mongo

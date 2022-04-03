# Bitexen-Code-Challenge

for flask 
docker build ./ --tag bitexen 
docker run --restart always -d --network=host --name bitexendeploy bitexen





for FASTAPI
docker build ./ --tag bitexenfastapi 
docker run --restart always -d --network=host --name fastdeploy bitexenfastapi


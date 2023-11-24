#!/bin/sh
tag=0.0.1
imagetag=latest
containername=producer
dockerhubacc=hansaskov
imagename=$dockerhubacc/$containername:$imagetag

echo $imagename
docker build --build-arg="CP_VERSION=$tag" --tag=$imagename  . 
# # docker run -it $imagename
# # docker login
docker push $imagename

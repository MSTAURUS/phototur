docker build -t phototur ./ && \
docker save -o ./phototur.tar phototur && \
docker stop $(docker ps -a -q) && \
docker rm $(docker ps -a -q) && \
docker rmi $(docker images -a -q) 

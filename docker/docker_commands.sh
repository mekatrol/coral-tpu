# Build image
docker build -t nodejs:1.0 . -f nodejs/Dockerfile
docker build -t pycoral:1.0 . -f pycoral/Dockerfile

# List image
docker image list

# Run image
docker run --name nodejs -dit -p 3000:3000 nodejs:1.0 
docker run --name pycoral --privileged -it pycoral:1.0 

# List running containers
docker ps

# Stop the image
docker stop pycoral

# Get logs
docker logs pycoral

# Start the image
docker start pycoral

# Attach to image
docker attach pycoral

# Prune containers
docker container prune

# Prune images
docker image prune
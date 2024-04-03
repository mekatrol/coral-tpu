# Build image
docker build -t nodejs:1.0 . -f nodejs/Dockerfile
docker build -t pycoral:1.0 . -f pycoral/Dockerfile

###################################################################################################################
# image_processing_server
# Run these from the image_processing_server directory
###################################################################################################################
docker image pull python:3.9
docker build -t image_processing_server:1.0 . 
# Run with auto remove (-rm) 
docker run --name image_processing_server --rm --network host --privileged -it image_processing_server:1.0
docker run --name image_processing_server --network host --privileged -dit image_processing_server:1.0

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
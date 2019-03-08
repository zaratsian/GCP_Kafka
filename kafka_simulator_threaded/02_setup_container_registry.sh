

######################################################################
#
# Google Cloud - Container Registry
#
######################################################################

# Variables
project_id=ml-healthcare-poc-201901 
container_name=kafka_simulator_threaded


# Authenticate - configure Docker to use the gcloud
gcloud auth configure-docker


# Tag the image with a registry name
docker tag $container_name gcr.io/$project_id/$container_name


# Push the image to Container Registry
docker push gcr.io/$project_id/$container_name


# Pull the image from Conainer Registry
#docker pull gcr.io/$project_id/$container_name
# Run the image from Conainer Registry
#docker run gcr.io/$project_id/$container_name


#ZEND

#Variables
#project_id="$(curl 'http://metadata.google.internal/computeMetadata/v1/project/project-id' -H 'Metadata-Flavor: Google')"
project_id=$GOOGLE_CLOUD_PROJECT

gcloud compute --project=$project_id firewall-rules \
        create kafka-firewall \
        --description="Allows requests from GKE to be sent to a Kafka Bootstrap Server GCE Instance" \
        --direction=INGRESS \
        --priority=1000 \
        --network=default \
        --action=ALLOW \
        --rules=tcp:9092 \
        --source-ranges=0.0.0.0/0

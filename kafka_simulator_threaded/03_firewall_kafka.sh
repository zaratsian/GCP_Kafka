gcloud compute --project=ml-healthcare-poc-201901 firewall-rules \
        create kafka-firewall \
        --direction=INGRESS \
        --priority=1000 \
        --network=default \
        --action=ALLOW \
        --rules=tcp:9092 \
        --source-ranges=0.0.0.0/0 \
        --target-tags=kafka

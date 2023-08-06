gcloud beta compute --project=$GCP_PROJECT instance-templates create-with-container $TEMPLATE_NAME \
    --machine-type=$MACHINE_TYPE --network=projects/$GCP_PROJECT/global/networks/default \
    --network-tier=PREMIUM --metadata=startup-script=$STARTUP_SCRIPT,google-logging-enabled=true \
    --restart-on-failure --maintenance-policy=TERMINATE --preemptible --service-account=$SERVICE_ACCOUNT \
    --scopes=https://www.googleapis.com/auth/cloud-platform --tags=http-server,https-server \
    --image=cos-81-12871-1245-10 --image-project=cos-cloud --boot-disk-size=10GB --boot-disk-type=pd-balanced \
    --boot-disk-device-name=$TEMPLATE_NAME --container-image=$IMAGE --container-restart-policy=on-failure \
    --container-privileged --labels=container-vm=cos-81-12871-1245-10

#!/bin/bash
: '
The following script connects to JuputerLab on
deep learning VM compute instance on GCP.
'

echo "INSTANCE_NAME=$1"
echo "ZONE=$2"
echo "PROJECT_ID=$3"
echo ""

gcloud compute ssh --project "$3" --zone "$2" \
  "$1" -- -L 8080:localhost:8080
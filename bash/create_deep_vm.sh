#!/bin/bash
: '
The following script creates
a new deep learning VM compute instance on GCP.
'

echo "INSTANCE_NAME=$1"
echo "ZONE=$2"
echo "IMAGE_FAMILY=$3"
echo "ACCELERATOR=$4"
echo "INSTANCE_TYPE=$5"
echo ""

gcloud compute instances create "$1" \
  --zone="$2" \
  --image-family="$3" \
  --image-project=deeplearning-platform-release \
  --maintenance-policy=TERMINATE \
  --accelerator="$4" \
  --machine-type="$5"
  --metadata="install-nvidia-driver=True"
#!/bin/bash

NAME=$1
REGION_US_EAST="aws:us-east-1"
REGION_EU_CENTRAL="aws:eu-central-1"

dx select $NAME
if [[ $? -ne 0 ]]; then
	echo "Creating new project ${NAME}"
	dx new project ${NAME} --region=${REGION_US_EAST} --bill-to=org-dnanexus_apps
fi

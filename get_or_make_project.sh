#!/bin/bash

NAME=$1

dx select $NAME
if [[ $? -ne 0 ]]; then
	echo "Creating new project $NAME"
	dx new project $NAME --region=aws:eu-central-1 --bill-to=org-dnanexus_apps
fi

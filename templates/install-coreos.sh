#!/bin/bash
BASE_URL="{{ base_url }}"
MAC="{{ mac }}"

curl -X PUT --data 'state=DEPLOYING' $BASE_URL/machine/$MAC
curl $BASE_URL/cloud-config/$MAC > cloud-config.yaml
sudo coreos-install -d /dev/sda -c cloud-config.yaml -C stable

if [ $? -eq 0 ]; then
    curl -X PUT --data 'state=DEPLOYED' $BASE_URL/machine/$MAC
    sudo reboot
else
    curl -X PUT --data 'state=DEPLOY_FAILED' $BASE_URL/machine/$MAC
fi

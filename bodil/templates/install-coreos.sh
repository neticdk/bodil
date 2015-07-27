#!/bin/bash
BASE_URL="{{ base_url }}"
API_URL=$BASE_URL/api/v1
MAC="{{ mac }}"

update_state() {
  curl -H 'Content-Type: application/json' \
       -X PUT \
       --data "state=$1" \
       $API_URL/machine/$MAC
}

update_state DEPLOYING
curl $API_URL/cloud-config/$MAC > cloud-config.yaml
sudo coreos-install -d /dev/sda -c cloud-config.yaml -C stable -b $BASE_URL/static/images/coreos/stable/current

if [ $? -eq 0 ]; then
    update_state DEPLOYED
    sudo reboot
else
    update_state DEPLOY_FAILED
fi


#!/bin/bash
BASE_URL="{{ base_url }}"
API_URL=$BASE_URL/api/v1
MAC="{{ mac }}"
COREOS_CHANNEL="{{ coreos_channel }}"
COREOS_VERSION="{{ coreos_version }}"

update_state() {
  curl -H 'Content-Type: application/json' \
       -X PUT \
       --data "{\"state\": \"$1\"}" \
       $API_URL/machine/$MAC
}

update_state DEPLOYING

curl $API_URL/cloud-config/$MAC > cloud-config.yaml
sudo coreos-install -d /dev/sda -c cloud-config.yaml -b $BASE_URL/static/images/coreos/$COREOS_CHANNEL -V $COREOS_VERSION -C $COREOS_CHANNEL

if [ $? -eq 0 ]; then
    update_state DEPLOYED
    sudo reboot
else
    update_state DEPLOY_FAILED
fi


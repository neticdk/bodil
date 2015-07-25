#!/bin/bash
curl -X PUT --data 'state=DEPLOYING' {{ base_url }}/machine/{{ mac }}
curl {{ base_url }}/cloud-config/{{ mac }} > cloud-config.yaml
sudo coreos-install -d /dev/sda -c cloud-config.yaml -C stable

if [ $? -eq 0 ]; then
    curl -X PUT --data 'state=DEPLOYED' {{ base_url }}/machine/{0}
        sudo reboot
else
    curl -X PUT --data 'state=DEPLOY_FAILED' {{ base_url }}/machine/{0}
fi

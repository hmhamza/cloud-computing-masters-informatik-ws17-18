#!/bin/bash
test $# == 0 || { echo "This script takes no parameters"; exit 1; }
CONFIG_FILE="/etc/nginx/nginx.conf"

# Compose the nginx server name of the container hostname and the hypervisor hostname
CC_SERVER_NAME="$(hostname)@$(cat "/hypervisor_etc/hostname")"

# Replace the template fields in the config file with actual values
sed -i "$CONFIG_FILE" \
	-e "s/<<CC_SERVER_NAME>>/$CC_SERVER_NAME/g"

# Print the resulting config file for verification and debugging
cat "$CONFIG_FILE"

#!/bin/bash
test $# == 1 || { echo "Need 1 parameter: <backend servers>"; exit 1; }
CC_BACKEND_SERVERS_LIST="$1"
CONFIG_FILE="/etc/nginx/nginx.conf"

# Compose the nginx server name of the container hostname and the hypervisor hostname
CC_SERVER_NAME="$(hostname)@$(cat "/hypervisor_etc/hostname")"

# Translate the list of backend servers into a form applicable for the config file
CC_BACKEND_SERVERS=$(sed -r 's/[^ \t][^ \t]*/server &:8000;\\n/g' <<< "$CC_BACKEND_SERVERS_LIST")

# Replace the template fields in the config file with actual values
sed -i "$CONFIG_FILE" \
	-e "s/<<CC_BACKEND_SERVERS>>/$CC_BACKEND_SERVERS/g" \
	-e "s/<<CC_SERVER_NAME>>/$CC_SERVER_NAME/g"

# Print the resulting config file for verification and debugging
cat "$CONFIG_FILE"

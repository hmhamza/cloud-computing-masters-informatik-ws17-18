#!/bin/bash
# This script removes all floating ips and ports of the current project.
# Floating ips and ports often prevent Heat from deleting a stack. If a stack delete command fails (stack is in state DELETE_FAILED),
# this script can be executed to avoid manual cleanup. Afterwards, the stack should be deleted with another stack delete command.
# Before executing this script, make sure that all instances are deleted, as they might still be using a floating ip or port.
#
# WARNING: this script deletes all floating IPs and ports in your entire project, not only the ones that are part of a Heat stack!
#
# openstack command line client version: 3.11.0
set -e -n

test -n "$OS_TENANT_NAME" || { echo "Environment variable OS_TENANT_NAME is not set. Please set it to the name or ID of your project."; exit 1; }

# Make sure no instance is running that could still be using a floating IP or port
instances=$(openstack server list --project $OS_TENANT_NAME -f value -c ID)
test -n "$instances" || { echo "There are still instances running for your project. Please delete them before executing this cleanup script."; exit 1; }

# Query all floating IPs and ports in the project
floating_ips=$(openstack floating ip list --project $OS_TENANT_NAME -f value -c ID)
port_ids=$(openstack port list --project $OS_TENANT_NAME -f value -c ID)

echo "Deleting the following floating IP(s):" $floating_ips
for i in $floating_ips; do
	openstack floating ip unset $i
	openstack floating ip delete $i
done
echo "Deleting the following port(s):" $port_ids
for i in $port_ids; do
	openstack port delete $i
done

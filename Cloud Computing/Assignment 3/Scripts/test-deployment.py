#!/use/bin/env python3
# Install requirement with: pip install requests
import requests

HASH_HEADER_NAME = "cchashkey"
FRONTEND_HEADER_NAME = "CC-Frontend-Server"
BACKEND_HEADER_NAME = "CC-Backend-Server"
NUM_REQUESTS = 100
HASH_KEYS = [ "x", "y", "z", "ABC", "123" ]
NUM_BACKENDS = 2
NUM_FRONTENDS = 1
NUM_BACKEND_CONTAINERS = 5
NUM_FRONTEND_CONTAINERS = 2

class DeploymentTester(object):

	def __init__(self, ip):
		self.ip = ip
		self.container_mapping = {}
		self.backend_servers = set()
		self.backend_containers = set()
		self.frontend_servers = set()
		self.frontend_containers = set()

	def get_request(self, hash_header):
		url = "http://%s" % self.ip
		headers = { HASH_HEADER_NAME: hash_header }
		return requests.get(url, headers=headers)

	def extract_header(self, response, header_name):
		if header_name not in response.headers:
			raise Exception("Missing header %s in response. Received headers: %s" % (header_name, list(response.headers.keys())))
		return response.headers[header_name]

	def get_frontend_backend(self, hash_header):
		response = self.get_request(hash_header)
		frontend = self.extract_header(response, FRONTEND_HEADER_NAME)
		backend = self.extract_header(response, BACKEND_HEADER_NAME)
		return (frontend, backend)

	def parse_endpoint(self, endpoint_header):
		parts = endpoint_header.split("@")
		if len(parts) != 2:
			raise Exception("Unexpected header value %s (expected 'containerID@hypervisor')" % endpoint_header)
		return (parts[0], parts[1])

	def check_container_mapping(self, container, node):
		if container in self.container_mapping:
			expected_node = self.container_mapping[container]
			if expected_node != node:
				raise Exception("Container %s was encountered on multiple nodes: %s, %s", container, expected_node, node)
		else:
			self.container_mapping[container] = node

	def test_request(self, hash_header):
		front, back = self.get_frontend_backend(hash_header)
		front_container, front_node = self.parse_endpoint(front)
		back_container, back_node = self.parse_endpoint(back)	
		self.check_container_mapping(front_container, front_node)
		self.check_container_mapping(back_container, back_node)
		self.backend_servers.add(back_node)
		self.frontend_servers.add(front_node)
		self.backend_containers.add(back_container)
		self.frontend_containers.add(front_container)
		return back_node

	def run_hash_test(self, hash_header):
		backend = None
		for _ in range(NUM_REQUESTS):
			request_backend = self.test_request(hash_header)
			if backend is None:
				backend = request_backend
			else:
				if backend != request_backend:
					raise Exception("The hash value %s resulted in requests to different backend servers %s and %s", backend, request_backend)

	def check_set_len(self, the_set, expected_len, set_name):
		if len(the_set) != expected_len:
			raise Exception("Unexpected number of encountered %s: Expected %s, have %s" % (set_name, expected_len, len(the_set)))

	def run_all_tests(self):
		print("Sending %s requests to %s..." % (len(HASH_KEYS) * NUM_REQUESTS, self.ip))
		for hash_key in HASH_KEYS:
			self.run_hash_test(hash_key)
			print("%s requests with hash key %s have been processed." % (NUM_REQUESTS, hash_key))
		self.check_set_len(self.backend_servers, NUM_BACKENDS, "backend servers")
		self.check_set_len(self.frontend_servers, NUM_FRONTENDS, "frontend servers")
		self.check_set_len(self.backend_containers, NUM_BACKEND_CONTAINERS, "backend containers")
		self.check_set_len(self.frontend_containers, NUM_FRONTEND_CONTAINERS, "frontend containers")

		print("All tests passed.")
		print("Found %s frontend servers: %s" % (len(self.frontend_servers), self.frontend_servers))
		print("Found %s frontend containers: %s" % (len(self.frontend_containers), self.frontend_containers))
		print("Found %s backend servers: %s" % (len(self.backend_servers), self.backend_servers))
		print("Found %s backend containers: %s" % (len(self.backend_containers), self.backend_containers))

def main(args):
	if len(args) != 1:
		print("Need 1 parameter: Floating IP of the frontend HTTP server")
		return 1
	floating_ip = args[0]
	return DeploymentTester(floating_ip).run_all_tests()

if __name__ == "__main__":
	import sys, os
	sys.exit(main(sys.argv[1:]))

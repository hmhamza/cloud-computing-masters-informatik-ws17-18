# Use an official nginx runtime as a parent image
FROM nginx:1.12.2

# Make port 80 available to the container host
EXPOSE 80

# Copy conf and sh file into container
COPY ./nginx.conf /etc/nginx/nginx.conf
COPY ./fix-nginx-conf.sh /scripts/fix-nginx-conf.sh

# Make scrips executable
RUN chmod u+x /scripts/*.sh

# Define a mount point
VOLUME /hypervisor_etc

# Run script and start nginx without params
ENTRYPOINT bash /scripts/fix-nginx-conf.sh;nginx
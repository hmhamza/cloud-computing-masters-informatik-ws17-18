#Front End Docker File Content:
FROM nginx:1.12.2

# Make port 80 available to the world outside this container
EXPOSE 80


# Copy conf and sh file into container
COPY ./nginx.conf /etc/nginx/nginx.conf
COPY ./fix-nginx-conf.sh /scripts/fix-nginx-conf.sh

# Make scrips executable
RUN chmod u+x /scripts/*.sh


# Define environment variable
ENV CC_BACKEND_SERVERS ${CC_BACKEND_SERVERS}

# Define a mount point
VOLUME /hypervisor_etc

# Run script and start nginx without params
ENTRYPOINT bash /scripts/fix-nginx-conf.sh "$CC_BACKEND_SERVERS";nginx

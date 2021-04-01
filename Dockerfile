FROM docker.io/sysrepo/sysrepo-netopeer2:latest

RUN apt-get update && apt-get install -y python3 python3-pip

RUN mkdir /logs

COPY ./models /resources/models
COPY ./scripts ./scripts
COPY ./src/python/netconf_server ./application/netconf_server
COPY src/python/netconf_change_listener_application.py ./application/netconf_change_listener_application.py
COPY ./src/python/netconf_rest_application.py ./application/netconf_rest_application.py
COPY ./src/python/requirements.txt ./application/requirements.txt
COPY ./src/python/setup.py ./application/setup.py

RUN pip3 install -e ./application/

RUN mkdir -p /resources/certs && \
    ./scripts/generate-certificates.sh /resources/certs

ENV ENABLE_TLS=false
ENV KAFKA_HOST_NAME="kafka1"
ENV KAFKA_PORT=9092
ENV KAFKA_TOPIC="config"

ENTRYPOINT ["./scripts/set-up-netopeer.sh", "/resources/models", "/resources/certs"]

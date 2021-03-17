FROM docker.io/sysrepo/sysrepo-netopeer2:latest
COPY ./models /resources/models
COPY ./scripts ./scripts
COPY ./src/python/netconf_server ./application/netconf_server
COPY ./src/python/netconf_server_application.py ./application/netconf_server_application.py
COPY ./src/python/requirements.txt ./application/requirements.txt
COPY ./src/python/setup.py ./application/setup.py

RUN apt-get update && apt-get install -y python3 python3-pip &&  pip3 install -e ./application/

ENV ENABLE_TLS=false

RUN mkdir -p /resources/certs && \
    ./scripts/generate-certificates.sh /resources/certs
RUN mkdir /logs

ENTRYPOINT ["./scripts/set-up-netopeer.sh", "/resources/models", "/resources/certs"]

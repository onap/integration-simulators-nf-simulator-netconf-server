FROM docker.io/sysrepo/sysrepo-netopeer2:latest
COPY ./models /resources/models
COPY ./scripts ./scripts
COPY ./src/python/application ./application
COPY ./src/python/requirements.txt ./application/requirements.txt

RUN apt-get update && apt-get install -y python3 python3-pip &&  pip3 install -r ./application/requirements.txt

ENV ENABLE_TLS=false

RUN mkdir -p /resources/certs && \
    ./scripts/generate-certificates.sh /resources/certs

ENTRYPOINT ["./scripts/set-up-netopeer.sh", "/resources/models", "/resources/certs"]

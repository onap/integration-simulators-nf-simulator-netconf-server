FROM docker.io/sysrepo/sysrepo-netopeer2:latest
COPY ./models /resources/models
COPY ./scripts ./scripts

ENV ENABLE_TLS=false

RUN mkdir -p /resources/certs && \
    ./scripts/generate-certificates.sh /resources/certs

ENTRYPOINT ["./scripts/set-up-netopeer.sh", "/resources/models", "/resources/certs"]

How to use
----------
    1. Make modifications in 'docker-compose.yml' in root directory

    Replace 'KAFKA_ADVERTISED_HOST_NAME: kafka1' by 'KAFKA_ADVERTISED_HOST_NAME: localhost'

    2. Build local netconf-server image in root directory

        mvn clean package -Pdocker

    3. Run docker-compose in root directory

        docker-compose up -d

    4. Run kafka_producer.py. Wait on results.
    5. Run kafka_consumer.py. Wait on results.

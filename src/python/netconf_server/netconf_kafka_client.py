###
# ============LICENSE_START=======================================================
# Netconf Server
# ================================================================================
# Copyright (C) 2021 Nokia. All rights reserved.
# ================================================================================
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============LICENSE_END=========================================================
###
import logging
from json import dumps
from typing import Callable, Any

from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import NoBrokersAvailable
from kafka.producer.future import FutureRecordMetadata
from retry import retry

from netconf_server.kafka_consumer_factory import provide_kafka_consumer

STANDARD_CHARSETS_UTF8 = 'utf-8'

logger = logging.getLogger(__name__)


@retry(NoBrokersAvailable, tries=3, delay=5)
def provide_configured_kafka_client(kafka_host_name, kafka_port):
    return NetconfKafkaClient.create(
        host=kafka_host_name,
        port=kafka_port
    )  # type: NetconfKafkaClient


class NetconfKafkaClient(object):

    @staticmethod
    def create(host: str, port: int):
        server = "{}:{}".format(host, port)
        producer = KafkaProducer(
            bootstrap_servers=server,
            value_serializer=lambda x: dumps(x).encode(STANDARD_CHARSETS_UTF8)
        )

        return NetconfKafkaClient(
            producer=producer,
            get_kafka_consumer_func=lambda topic: provide_kafka_consumer(topic, server)
        )

    def __init__(self, producer: KafkaProducer, get_kafka_consumer_func: Callable[[str], KafkaConsumer]):
        self._producer = producer
        self._get_kafka_consumer = get_kafka_consumer_func

    def send(self, topic: str, value: Any) -> FutureRecordMetadata:
        return self._producer.send(
            topic=topic,
            value=value
        )

    def get_all_messages_from(self, topic: str) -> list:
        logger.debug("Getting config changes from topic %s" % topic)

        messages = []
        consumer = self._get_kafka_consumer(topic)
        for message in consumer:
            message_value = message.value
            logger.info("Fetched config change %s" % message_value)
            messages.append(message_value)

        return messages

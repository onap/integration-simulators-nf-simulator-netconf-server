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

from kafka.producer.future import FutureRecordMetadata

from netconf_server.netconf_kafka_client import NetconfKafkaClient
from netconf_server.netconf_kafka_message_factory import NetconfKafkaMessageFactory
from netconf_server.sysrepo_interface.config_change_data import ConfigChangeData
from netconf_server.sysrepo_interface.sysrepo_message_model import SysrepoMessage

logger = logging.getLogger(__name__)


class NetconfChangeListener(object):

    def __init__(self, subscriptions: list, kafka_client: NetconfKafkaClient, topic: str):
        self.subscriptions = subscriptions
        self.kafka_client = kafka_client
        self.topic = topic

    def run(self, session):
        for subscription in self.subscriptions:
            subscription.callback_function = self._on_module_configuration_change
            subscription.subscribe_on_model_change(session)

    def _on_module_configuration_change(self, config_change_data: ConfigChangeData):
        logger.info("Received module changed: {} , {} ".format(config_change_data.event, config_change_data.changes))
        if config_change_data.event != "done":
            self._send_change_to_kafka(config_change_data)

    def _send_change_to_kafka(self, config_change_data):
        for change in config_change_data.changes:
            try:
                kafka_message = NetconfChangeListener._create_kafka_message(change)
                logging.info("Sending message '{}' to Kafka '{}' topic".format(kafka_message, self.topic))
                response = self.kafka_client.send(self.topic, kafka_message)  # type: FutureRecordMetadata
                self.set_up_callbacks_for_kafka_request(response)
                logging.info("Module changes sent to Kafka")
            except Exception as e:
                logger.error("Exception occurred during handling of sysrepo config change", e)

    @staticmethod
    def set_up_callbacks_for_kafka_request(response):
        response.add_callback(
            lambda val: logging.info("Response from Kafka: {}".format(val))
        )
        response.add_errback(
            lambda exc: logging.error("Exception from Kafka: {}".format(exc))
        )

    @staticmethod
    def _create_kafka_message(change):
        return NetconfKafkaMessageFactory.create(SysrepoMessage(change))

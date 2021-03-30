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


from netconf_server.netconf_app_configuration import NetconfAppConfiguration
from netconf_server.netconf_change_listener import NetconfChangeListener
from netconf_server.netconf_kafka_client import NetconfKafkaClient, provide_configured_kafka_client
from netconf_server.sysrepo_interface.config_change_subscriber import ConfigChangeSubscriber

logger = logging.getLogger(__name__)


class NetconfChangeListenerFactory(object):

    def __init__(self, modules_to_subscribe_names: list, app_configuration: NetconfAppConfiguration):
        self.modules_to_subscribe_names = modules_to_subscribe_names
        self.app_configuration = app_configuration

    def create(self) -> NetconfChangeListener:
        subscriptions = list()
        for module_name in self.modules_to_subscribe_names:
            subscriptions.append(
                ConfigChangeSubscriber(module_name)
            )
        kafka_client = self._try_to_create_kafka_client(
            self.app_configuration.kafka_host_name,
            self.app_configuration.kafka_port
        )

        return NetconfChangeListener(subscriptions, kafka_client, self.app_configuration.kafka_topic)

    def _try_to_create_kafka_client(self, kafka_host_name, kafka_port):
        return provide_configured_kafka_client(kafka_host_name, kafka_port)  # type: NetconfKafkaClient

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
import unittest
from unittest.mock import MagicMock

import sys

# we need to mock sysrepo library. It is not possible to install it in the newest version of the Linux distribution
sys.modules['sysrepo'] = MagicMock()

from netconf_server.netconf_app_configuration import NetconfAppConfiguration
from netconf_server.netconf_change_listener_factory import NetconfChangeListenerFactory
from tests.mocs.mocked_session import MockedSession


class TestNetconfChangeListenerFactory(unittest.TestCase):

    def test_should_create_and_run_netconf_server_with_one_model(self):
        # given
        modules_to_subscribe_names = ["test"]
        factory = TestNetconfChangeListenerFactory._given_netconf_change_listener_factory(modules_to_subscribe_names)
        server = factory.create()
        session = MockedSession()
        session.subscribe_module_change = MagicMock()

        # when
        server.run(session)

        # then
        session.subscribe_module_change.assert_called_once()

    def test_should_create_and_run_netconf_server_with_multiple_models(self):
        # given
        modules_to_subscribe_names = ["test", "test2", "test3"]
        factory = TestNetconfChangeListenerFactory._given_netconf_change_listener_factory(modules_to_subscribe_names)
        server = factory.create()
        session = MockedSession()
        session.subscribe_module_change = MagicMock()

        # when
        server.run(session)

        # then
        self.assertEqual(session.subscribe_module_change.call_count, 3)

    @staticmethod
    def _given_netconf_change_listener_factory(modules_to_subscribe_names: list) -> NetconfChangeListenerFactory:
        app_configuration, _ = NetconfAppConfiguration.get_configuration(
            ["../models", "models-configuration.ini", "127.0.0.1", "9092",
             "kafka1"])  # type: NetconfAppConfiguration, str
        factory = NetconfChangeListenerFactory(modules_to_subscribe_names, app_configuration)
        factory._create_kafka_client = lambda host, port: MagicMock()
        return factory

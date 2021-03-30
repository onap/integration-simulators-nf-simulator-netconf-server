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
from netconf_server.sysrepo_interface.config_change_data import ConfigChangeData

sys.modules['sysrepo'] = MagicMock()
from netconf_server.netconf_change_listener import NetconfChangeListener

KAFKA_TOPIC = "config"


class TestNetconfChangeListener(unittest.TestCase):
    def test_should_subscribe_on_run(self):
        # given
        subscriber1 = MagicMock()
        subscriber2 = MagicMock()
        kafka_client = MagicMock()
        session = MagicMock()
        netconf_change_listener = NetconfChangeListener([subscriber1, subscriber2], kafka_client, KAFKA_TOPIC)

        # when
        netconf_change_listener.run(session)

        # then
        subscriber1.subscribe_on_model_change.assert_called_once()
        self.assertEqual(subscriber1.callback_function, netconf_change_listener._on_module_configuration_change)
        subscriber2.subscribe_on_model_change.assert_called_once()
        self.assertEqual(subscriber2.callback_function, netconf_change_listener._on_module_configuration_change)

    def test_should_send_two_changes_at_kafka(self):
        # given
        subscriber1 = MagicMock()
        subscriber2 = MagicMock()
        kafka_client = MagicMock()
        netconf_change_listener = NetconfChangeListener([subscriber1, subscriber2], kafka_client, KAFKA_TOPIC)
        NetconfChangeListener._create_kafka_message = lambda _: MagicMock()

        # when
        netconf_change_listener._on_module_configuration_change(
            ConfigChangeData(
                event="event",
                req_id=1,
                changes=[MagicMock(), MagicMock()]
            )
        )

        # then
        self.assertEqual(kafka_client.send.call_count, 2)


if __name__ == '__main__':
    unittest.main()

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

from netconf_server.netconf_server_factory import NetconfServerFactory
from tests.mocs.mocked_session import MockedSession


class TestNetconfServer(unittest.TestCase):

    def test_should_create_and_run_netconf_server_with_one_model(self):
        # given
        modules_to_subscribe_names = ["test"]
        server = NetconfServerFactory(modules_to_subscribe_names).create()
        session = MockedSession()
        session.subscribe_module_change = MagicMock()

        # when
        server.run(session)

        # then
        session.subscribe_module_change.assert_called_once()

    def test_should_create_and_run_netconf_server_with_multiple_models(self):
        # given
        modules_to_subscribe_names = ["test", "test2", "test3"]
        server = NetconfServerFactory(modules_to_subscribe_names).create()
        session = MockedSession()
        session.subscribe_module_change = MagicMock()

        # when
        server.run(session)

        # then
        self.assertEqual(session.subscribe_module_change.call_count, 3)

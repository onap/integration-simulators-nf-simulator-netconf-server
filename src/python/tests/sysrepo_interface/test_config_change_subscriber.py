###
# ============LICENSE_START=======================================================
# Simulator
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
import time
import unittest
from unittest.mock import MagicMock

from application.sysrepo_interface.config_change_data import ConfigChangeData
from application.sysrepo_interface.config_change_subscriber import ConfigChangeSubscriber
from tests.mocs.mocked_session import MockedSession


class TestConfigChangeSubscriber(unittest.TestCase):

    @staticmethod
    def __test_callback(config_change_data: ConfigChangeData):
        pass

    def test_should_create_subscriber_and_call_callback_when_session_detects_change(self):
        self.__test_callback = MagicMock()
        subscriber = ConfigChangeSubscriber("test", self.__test_callback)
        session = MockedSession()
        subscriber.subscribe_on_model_change(session)
        self.__test_callback.assert_not_called()
        session.call_config_changed()
        self.__test_callback.assert_called_once()

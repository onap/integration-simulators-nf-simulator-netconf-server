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
import asyncio


class MockedSession(object):

    def __init__(self):
        self.__callback = None

    def subscribe_module_change(self, module_name, _, on_module_have_changed, asyncio_register=True):
        self.__callback = on_module_have_changed
        pass

    def call_config_changed(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.__callback('event', 'req_id', 'changes', 'private_data'))

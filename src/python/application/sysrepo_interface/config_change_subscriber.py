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

import asyncio
import logging

from application.sysrepo_interface.config_change_data import ConfigChangeData


class ConfigChangeSubscriber(object):

    def __init__(self, module_name, callback_function):
        self.module_name = module_name
        self.callback_function = callback_function

    def subscribe_on_model_change(self, session):
        logging.info("Subscribing on config change for module %s" % self.module_name)
        session.subscribe_module_change(
            self.module_name, None, self.on_module_have_changed, asyncio_register=True
        )

    async def on_module_have_changed(self, event, req_id, changes, private_data):
        logging.debug("Module changed: %s (request ID %s)" % (event, req_id))
        self.callback_function(ConfigChangeData(event, req_id, changes))
        await asyncio.sleep(0)

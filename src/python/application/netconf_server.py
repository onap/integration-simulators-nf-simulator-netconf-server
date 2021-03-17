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
import logging

from application.sysrepo_interface.config_change_data import ConfigChangeData
from application.sysrepo_interface.config_change_subscriber import ConfigChangeSubscriber


class NetconfServer(object):

    def __init__(self, modules_to_subscribe_names):
        self.subscriptions = list()
        for module_name in modules_to_subscribe_names:
            self.subscriptions.append(
                ConfigChangeSubscriber(module_name, self.__on_module_configuration_change)
            )

    def run(self, session):
        for subscription in self.subscriptions:
            subscription.subscribe_on_model_change(session)

    @staticmethod
    def __on_module_configuration_change(config_change_data: ConfigChangeData):
        logging.info("Received module changed: %s , %s " % (config_change_data.event, config_change_data.changes))

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

from netconf_server.sysrepo_interface.sysrepo_message_model import SysrepoMessage

logger = logging.getLogger(__name__)


class NetconfKafkaMessageFactory(object):

    @classmethod
    def create(cls, change: SysrepoMessage) -> dict:
        message = {}
        if change and change.is_modified():
            logger.debug("Parsing change modified")
            message = cls._create_modified_message(change)
        elif change and change.is_created():
            logger.debug("Parsing change created")
            message = cls._create_created_message(change)
        return message

    @classmethod
    def _create_created_message(cls, change: SysrepoMessage) -> dict:
        message = {"type": "ChangeCreated"}
        if change.value():
            message["new"] = {"path": change.xpath(), "value": change.value()}
        return message

    @classmethod
    def _create_modified_message(cls, change: SysrepoMessage) -> dict:
        message = {"type": "ChangeModified"}
        if change.prev_val():
            message["old"] = {"path": change.xpath(), "value": change.prev_val()}
        if change.value():
            message["new"] = {"path": change.xpath(), "value": change.value()}
        return message

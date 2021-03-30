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
from json import loads

from kafka import KafkaConsumer

STANDARD_CHARSETS_UTF8 = 'utf-8'


def provide_kafka_consumer(topic: str, server: str) -> KafkaConsumer:
    return KafkaConsumer(topic,
                         consumer_timeout_ms=1000,
                         group_id='netconf-group',
                         auto_offset_reset='earliest',
                         enable_auto_commit=False,
                         bootstrap_servers=[server],
                         value_deserializer=lambda x: loads(x.decode(STANDARD_CHARSETS_UTF8))
                         )

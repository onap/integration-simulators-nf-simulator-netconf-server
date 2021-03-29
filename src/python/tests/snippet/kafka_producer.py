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

from netconf_server.netconf_kafka_client import NetconfKafkaClient

NUMBER_OF_MESSAGES = 1000

logging.basicConfig(filename='kafka_producer.log', level=logging.DEBUG)

if __name__ == "__main__":

    client = NetconfKafkaClient.create(
        host="localhost",
        port=9092
    )

    for number in range(NUMBER_OF_MESSAGES):
        print("Send {}".format(number))
        data = {'number': number}
        resp = client.send(
            topic='config',
            value=data
        )
        print("Response: {}".format(resp.get(timeout=4)))

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
from unittest import TestCase
from unittest.mock import MagicMock, call

from netconf_server.netconf_kafka_client import NetconfKafkaClient

MESSAGE_1 = "{'number':1}"
MESSAGE_2 = "{'number':2}"

TOPIC_NAME = 'config'


class TestNetconfKafkaClient(TestCase):

    def setUp(self):
        self.producer = MagicMock()
        self.kafkaConsumerResponse = KafkaConsumerResponse(MagicMock(value=MESSAGE_1), MagicMock(value=MESSAGE_2))
        self.kafkaConsumerResponse.close = MagicMock()
        self.kafka_customer_func = MagicMock(
            return_value=self.kafkaConsumerResponse
        )
        self.test_obj = NetconfKafkaClient(
            producer=self.producer,
            get_kafka_consumer_func=self.kafka_customer_func
        )

    def test_create_instance(self):
        self.assertIsNotNone(self.test_obj)

    def test_send_a_message_to_kafka(self):
        # when
        self.test_obj.send(TOPIC_NAME, MESSAGE_1)

        # then
        self.producer.assert_has_calls([call.send(topic=TOPIC_NAME, value=MESSAGE_1)])

    def test_get_all_messages_from_kafka_topic(self):
        # when
        messages = self.test_obj.get_all_messages_from(TOPIC_NAME)

        # then
        self.assertTrue(len(messages) == 2)
        self.assertTrue(MESSAGE_1 in messages)
        self.assertTrue(MESSAGE_2 in messages)


class KafkaConsumerResponse(list):

    def __new__(self, *args, **kwargs):
        return super(KafkaConsumerResponse, self).__new__(self, args, kwargs)

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and hasattr(args[0], '__iter__'):
            list.__init__(self, args[0])
        else:
            list.__init__(self, args)
        self.__dict__.update(kwargs)

    def __call__(self, **kwargs):
        self.__dict__.update(kwargs)
        return self

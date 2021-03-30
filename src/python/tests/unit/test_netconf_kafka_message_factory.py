from collections import namedtuple
from unittest import TestCase
from unittest.mock import MagicMock

import sys

# we need to mock sysrepo library. It is not possible to install it in the newest version of the Linux distribution
sys.modules['sysrepo'] = MagicMock()

from netconf_server.sysrepo_interface.sysrepo_message_model import SysrepoMessage

from netconf_server.netconf_kafka_message_factory import NetconfKafkaMessageFactory

SYSREPO_MESSAGE_MODEL = namedtuple('SM', ['value', 'xpath', 'prev_val'])


class TestNetconfKafkaMessageFactory(TestCase):
    def test_should_return_empty_dict_when_sysrepo_message_is_none(self):
        # when
        actual = NetconfKafkaMessageFactory.create(None)

        # then
        self.assertEqual({}, actual)

    def test_should_prepare_message_for_sysrepo_message_with_status_change_created(self):
        # given
        s = SYSREPO_MESSAGE_MODEL(44, '/pnf-simulator:config/itemValue1', None)

        sysrepo_message = SysrepoMessage(s)
        sysrepo_message.is_modified = lambda: False
        sysrepo_message.is_created = lambda: True

        # when
        actual = NetconfKafkaMessageFactory.create(sysrepo_message)

        # then
        self.assertEqual(
            {'type': 'ChangeCreated', 'new': {'path': '/pnf-simulator:config/itemValue1', 'value': 44}},
            actual
        )

    def test_should_prepare_message_for_sysrepo_message_with_status_change_modified_no_old_value(self):
        # given
        s = SYSREPO_MESSAGE_MODEL(45, '/pnf-simulator:config/itemValue1', None)

        sysrepo_message = SysrepoMessage(s)
        sysrepo_message.is_modified = lambda: True
        sysrepo_message.is_created = lambda: False

        # when
        actual = NetconfKafkaMessageFactory.create(sysrepo_message)

        # then
        self.assertEqual(
            {'type': 'ChangeModified', 'new': {'path': '/pnf-simulator:config/itemValue1', 'value': 45}},
            actual
        )

    def test_should_prepare_message_for_sysrepo_message_with_status_change_modified_old_value_exists(self):
        # given
        s = SYSREPO_MESSAGE_MODEL(45, '/pnf-simulator:config/itemValue1', 44)

        sysrepo_message = SysrepoMessage(s)
        sysrepo_message.is_modified = lambda: True
        sysrepo_message.is_created = lambda: False

        # when
        actual = NetconfKafkaMessageFactory.create(sysrepo_message)

        # then
        self.assertEqual(
            {'type': 'ChangeModified', 'old': {'path': '/pnf-simulator:config/itemValue1', 'value': 44}, 'new': {'path': '/pnf-simulator:config/itemValue1', 'value': 45}},
            actual
        )


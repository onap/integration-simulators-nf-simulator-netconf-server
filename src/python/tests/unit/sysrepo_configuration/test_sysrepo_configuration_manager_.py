import json
import unittest
from unittest.mock import MagicMock
from netconf_server.sysrepo_configuration.sysrepo_configuration_manager import SysrepoConfigurationManager


class TestSysrepoConfigurationManager(unittest.TestCase):

    def test_should_change_configuration(self):
        # given
        expected_parse_data = "parse_data"

        ctx = MagicMock()
        ctx.parse_data_mem = MagicMock(return_value=expected_parse_data)
        connection = MagicMock()
        connection.get_ly_ctx = MagicMock(return_value=ctx)
        session = MagicMock()
        session.replace_config_ly = MagicMock()

        config_data = '''<config xmlns="http://onap.org/pnf-simulator">
                        <itemValue1>12</itemValue1>
                        <itemValue2>12</itemValue2>
                        </config>'''
        module_name = "pnf-simulator"

        # when
        config_manager = SysrepoConfigurationManager(session=session, connection=connection)
        config_manager.change_configuration(config_data=config_data, module_name=module_name)

        # then
        ctx.parse_data_mem.assert_called_with(config_data, "xml", config=True, strict=False)
        session.replace_config_ly.assert_called_with(expected_parse_data, module_name)

    def test_should_get_configuration(self):
        # given
        expected_parse_data = '{"config": {"itemValue1": 42,"itemValue2": 35}}'

        connection = MagicMock()
        session = MagicMock()
        session.get_data = MagicMock(return_value=expected_parse_data)
        module_name = "pnf-simulator"

        # when
        config_manager = SysrepoConfigurationManager(session=session, connection=connection)
        data = config_manager.get_configuration(module_name=module_name)

        # then
        session.get_data.assert_called_with("/" + module_name + ":*")
        self.assertEqual(data, json.dumps(expected_parse_data))

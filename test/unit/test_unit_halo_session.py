import imp
import os
import re
import sys


module_name = 'cloudpassage_slim'
here_dir = os.path.dirname(os.path.abspath(__file__))
module_path = os.path.join(here_dir, '../../')
sys.path.append(module_path)
fp, pathname, description = imp.find_module(module_name)
cloudpassage_slim = imp.load_module(module_name, fp, pathname, description)


class TestUnitHaloSession(object):
    def test_unit_halo_session_instantiate(self):
        session = cloudpassage_slim.HaloSession("key", "secret",
                                                api_host="api2.cloudpassage.com",  # NOQA
                                                integration_string="abc123")
        assert session
        user_agent = session.user_agent
        assert "abc123" in user_agent
        assert "api2.cloudpassage.com" == session.api_host

    def test_unit_halo_session_build_auth_headers(self):
        api_key = "yassss"
        api_secret = "nooooo"
        expected = {"Authorization": "Basic eWFzc3NzOm5vb29vbw=="}
        actual = cloudpassage_slim.HaloSession.build_auth_headers(api_key,
                                                                  api_secret)
        assert expected == actual

    def test_unit_halo_session_build_ua_string(self):
        sdk = "yassss"
        integration = "nooooo"
        expected = "yassss nooooo"
        actual = cloudpassage_slim.HaloSession.build_ua_string(sdk,
                                                               integration)
        assert expected == actual

    def test_unit_halo_session_get_sdk_version(self):
        re_expect = re.compile(r'^\d+\.\d+.*')
        actual = cloudpassage_slim.HaloSession.get_sdk_version()
        assert re_expect.match(actual)

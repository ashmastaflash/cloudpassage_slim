import imp
import os
import pytest
import sys


module_name = 'cloudpassage_slim'
here_dir = os.path.dirname(os.path.abspath(__file__))
module_path = os.path.join(here_dir, '../../')
sys.path.append(module_path)
fp, pathname, description = imp.find_module(module_name)
cloudpassage_slim = imp.load_module(module_name, fp, pathname, description)

fixture_path = os.path.join(here_dir, "../fixtures")


class TestIntegrationHttpHelper(object):
    def get_halo_session(self):
        halo_key = os.getenv("HALO_API_KEY")
        halo_secret = os.getenv("HALO_API_SECRET")
        if None not in [halo_key, halo_secret]:
            session = cloudpassage_slim.HaloSession(halo_key, halo_secret)
        else:
            print("No API authentication env vars set!")
            print("You must set HALO_API_KEY, HALO_API_SECRET to test this!")
            raise ValueError
        return session

    def get_halo_session_with_my_certs(self):
        halo_key = os.getenv("HALO_API_KEY")
        halo_secret = os.getenv("HALO_API_SECRET")
        cert_file = os.path.join(fixture_path, "cacert.pem")
        if None not in [halo_key, halo_secret]:
            session = cloudpassage_slim.HaloSession(halo_key, halo_secret,
                                                    cert_file=cert_file)
        else:
            print("No API authentication env vars set!")
            print("You must set HALO_API_KEY, HALO_API_SECRET to test this!")
            raise ValueError
        return session

    def get_halo_session_bad(self):
        halo_key = os.getenv("HALO_API_KEY")
        halo_secret = "SEEKRITSEEKRITSEEKRITLETMEIN"
        if None not in [halo_key, halo_secret]:
            session = cloudpassage_slim.HaloSession(halo_key, halo_secret)
        else:
            print("No API authentication env vars set!")
            print("You must set HALO_API_KEY, HALO_API_SECRET to test this!")
            raise ValueError
        return session

    def get_http_helper(self, session):
        http_helper = cloudpassage_slim.HttpHelper(session)
        return http_helper

    def test_connect_generic(self):
        method = "GET"
        host = "www.python.org"
        path = "/"
        status, reason, body = cloudpassage_slim.HttpHelper.connect(method,
                                                                    host, path)
        assert status == 200
        assert reason
        assert body

    def test_http_helper_get_auth_fail(self):
        session = self.get_halo_session_bad()
        http_helper = self.get_http_helper(session)
        authwall_path = "/v1/servers/"
        with pytest.raises(cloudpassage_slim.CloudPassageAuthentication):
            http_helper.get(authwall_path)
        assert True

    def test_http_helper_get_404(self):
        session = self.get_halo_session()
        http_helper = self.get_http_helper(session)
        path = "/v1/servers/abcdefg"
        with pytest.raises(cloudpassage_slim.CloudPassageResourceExistence):
            http_helper.get(path)
        assert True

    def test_http_helper_force_rekey(self):
        session = self.get_halo_session()
        session.api_token = "oldkey"
        http_helper = self.get_http_helper(session)
        path = "/v1/servers/"
        assert http_helper.get(path)

    def test_http_helper_with_my_certs(self):
        session = self.get_halo_session_with_my_certs()
        http_helper = self.get_http_helper(session)
        path = "/v1/servers/"
        assert http_helper.get(path)

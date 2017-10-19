import imp
import os
import sys


module_name = 'cloudpassage_slim'
here_dir = os.path.dirname(os.path.abspath(__file__))
module_path = os.path.join(here_dir, '../../')
sys.path.append(module_path)
fp, pathname, description = imp.find_module(module_name)
cloudpassage_slim = imp.load_module(module_name, fp, pathname, description)

fixture_path = os.path.join(here_dir, "../fixtures")


class TestIntegrationHaloSession(object):
    def test_authenticate_session(self):
        halo_key = os.getenv("HALO_API_KEY")
        halo_secret = os.getenv("HALO_API_SECRET")
        if None not in [halo_key, halo_secret]:
            session = cloudpassage_slim.HaloSession(halo_key, halo_secret)
            assert session.authenticate()
            assert session.api_token is not None
        else:
            print("No API authentication env vars set!")
            print("You must set HALO_API_KEY, HALO_API_SECRET to test this!")
            assert False is True

    def test_authenticate_session_with_cacerts(self):
        halo_key = os.getenv("HALO_API_KEY")
        halo_secret = os.getenv("HALO_API_SECRET")
        cert_file = os.path.join(fixture_path, "cacert.pem")
        if None not in [halo_key, halo_secret]:
            session = cloudpassage_slim.HaloSession(halo_key, halo_secret,
                                                    cert_file=cert_file)
            assert session.authenticate()
            assert session.api_token is not None
        else:
            print("No API authentication env vars set!")
            print("You must set HALO_API_KEY, HALO_API_SECRET to test this!")
            assert False is True

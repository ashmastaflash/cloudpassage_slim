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

CloudPassageValidation = cloudpassage_slim.CloudPassageValidation
CloudPassageAuthentication = cloudpassage_slim.CloudPassageAuthentication
CloudPassageResourceExistence = cloudpassage_slim.CloudPassageResourceExistence
CloudPassageAuthorization = cloudpassage_slim.CloudPassageAuthorization
CloudPassageValidation = cloudpassage_slim.CloudPassageValidation


class TestUnitHttpHelper(object):
    def test_unit_http_helper_response_disposition(self):
        for code, ex in {400: CloudPassageValidation,
                         404: CloudPassageResourceExistence,
                         403: CloudPassageAuthorization,
                         422: CloudPassageValidation}.items():  # NOQA
            disp, exc = cloudpassage_slim.HttpHelper.response_disposition(code,
                                                                          "hi",
                                                                          code)
            assert disp != "good"
            assert exc is not None
            with pytest.raises(ex):
                raise exc
                assert True

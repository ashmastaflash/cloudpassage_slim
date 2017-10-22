import base64
import httplib
import json
import os
import re
import ssl
import urllib
from urlparse import urlunsplit
from exceptions import CloudPassageAuthentication


class HaloSession(object):
    """All Halo API session management happens in this object.

    Args:
        key(str): Halo API key
        secret(str): Halo API secret

    Kwargs:
        api_host(str): Hostname for Halo API.  Defaults to
            ``api.cloudpassage.com``
        cert_file(str): Full path to CA file.
        integration_string(str): This identifies a specific integration to the
            Halo API.
    """
    def __init__(self, halo_key, halo_secret, **kwargs):
        self.key = halo_key
        self.secret = halo_secret
        self.api_host = "api.cloudpassage.com"
        self.sdk_version = self.get_sdk_version()
        self.sdk_version_string = "Halo-Python-SDK-slim/%s" % self.sdk_version
        self.integration_string = ''
        self.cert_file = None
        if "api_host" in kwargs:
            self.api_host = kwargs["api_host"]
        if "cert_file" in kwargs:
            self.cert_file = kwargs["cert_file"]
        if "integration_string" in kwargs:
            self.integration_string = kwargs["integration_string"]
        self.user_agent = self.build_ua_string(self.sdk_version_string,
                                               self.integration_string)
        self.threads = 10
        self.api_token = None

    def authenticate(self):
        """Obtain and set an oauth API token."""
        headers = self.build_auth_headers(self.key, self.secret)
        headers["User-Agent"] = self.user_agent
        params = urllib.urlencode({'grant_type': 'client_credentials'})
        if self.cert_file is None:
            connection = httplib.HTTPSConnection(self.api_host)
        else:
            ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
            ctx.load_verify_locations(self.cert_file)
            connection = httplib.HTTPSConnection(self.api_host,
                                                 context=ctx)
        connection.request("POST", '/oauth/access_token', params, headers)
        response = connection.getresponse()
        code = response.status
        body = response.read().decode()
        if code == 401:  # Bad API key...
            raise CloudPassageAuthentication(json.dumps(body))
        self.api_token = json.loads(body)['access_token']
        return True

    @classmethod
    def build_auth_headers(cls, key, secret):
        """Create an auth string for Halo oauth."""
        credfmt = "{key}:{secret}".format(key=key, secret=secret)
        creds = base64.b64encode(credfmt)
        auth_string = "Basic {creds}".format(creds=creds)
        auth_header = {"Authorization": auth_string}
        return auth_header

    def build_header(self):
        """This builds the header, required for all API interaction."""
        if self.api_token is None:
            self.authenticate()
        authstring = "Bearer " + self.api_token
        header = {"Authorization": authstring,
                  "Content-Type": "application/json",
                  "User-Agent": self.user_agent}
        return header

    @classmethod
    def build_ua_string(cls, sdk_version_str, integration_string):
        ua = "{sdk} {integration}".format(sdk=sdk_version_str,
                                          integration=integration_string)
        return ua

    def build_url(self, endpoint):
        """Build a URL from parts."""
        url = urlunsplit(("https", self.api_host, endpoint, "", ""))
        return url

    @classmethod
    def get_sdk_version(cls):
        here_dir = os.path.abspath(os.path.dirname(__file__))
        init_file_path = os.path.join(here_dir, "__init__.py")
        raw_init_file = open(init_file_path).read()
        print raw_init_file
        rx_compiled = re.compile(r"\s*__version__\s*=\s*\"(\S+)\"")
        version = rx_compiled.search(raw_init_file).group(1)
        return version

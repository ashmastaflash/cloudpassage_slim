import httplib
import time
import urllib
from exceptions import CloudPassageGeneral


class HttpHelper(object):
    """Instantiate this class with a HaloSession object."""
    def __init__(self, session):
        self.session = session

    @classmethod
    def connect(self, method, host, path, headers, params=""):
        """Return a tuple of response code, reason, and page body."""
        params_enc = urllib.urlencode(dict(params))
        conn = httplib.HTTPSConnection(host)
        conn.request(method, path, params_enc, headers)
        response = conn.getresponse()
        status_code = response.status
        reason = response.reason
        body = response.read()
        conn.close()
        return (status_code, reason, body)

    def get(self, path, **kwargs):
        headers = self.session.build_header()
        params = ""
        tries = 0
        if params in kwargs:
            params = kwargs["params"]
        while tries < 3:
            status_code, reason, body = self.connect("GET", self.session.host,
                                                     path, headers, params)
            disposition = self.response_disposition(status_code)
            if disposition == "rekey":
                self.session.authenticate()
                tries += 1
                continue
            elif disposition == "wait":
                time.sleep(5)
                tries += 1
                continue
            elif disposition == "bad":
                raise CloudPassageGeneral(reason, code=status_code)
            elif disposition == "good":
                break
        return body

    @classmethod
    def response_disposition(cls, response_code):
        """Return either "good", "bad", "rekey", or "wait"."""
        disposition = "bad"
        if 200 <= response_code < 300:
            disposition = "good"
        elif response_code == 401:
            disposition = "rekey"
        elif 400 <= response_code < 500:
            disposition = "bad"
        elif 500 <= response_code <= 599:
            disposition = "wait"
        return disposition

import httplib
import json
import ssl
import time
import urllib
from exceptions import CloudPassageAuthorization
from exceptions import CloudPassageGeneral
from exceptions import CloudPassageResourceExistence
from exceptions import CloudPassageValidation


class HttpHelper(object):
    """Instantiate this class with a HaloSession object."""
    def __init__(self, session):
        self.session = session

    @classmethod
    def connect(self, method, host, path, **kwargs):
        """Return a tuple of response code, reason, and page body."""
        headers, params = {}, ""
        if "params" in kwargs:
            params = urllib.urlencode(dict(kwargs["params"]))
        if "headers" in kwargs:
            headers = kwargs["headers"]
        if "cert_file" in kwargs:
            ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
            ctx.load_verify_locations(kwargs["cert_file"])
            conn = httplib.HTTPSConnection(host, context=ctx)
        else:
            conn = httplib.HTTPSConnection(host)
        conn.request(method, path, params, headers)
        response = conn.getresponse()
        status_code = response.status
        reason = response.reason
        body = response.read()
        conn.close()
        return (status_code, reason, body)

    def get(self, path, **kwargs):
        params = {}
        tries = 0
        if "params" in kwargs:
            params = kwargs["params"]
        while tries < 3:
            headers = self.session.build_header()
            if self.session.cert_file is not None:
                cert_file = self.session.cert_file
                status_code, reason, body = self.connect("GET",
                                                         self.session.api_host,
                                                         path, headers=headers,
                                                         params=params,
                                                         cert_file=cert_file)
            else:
                status_code, reason, body = self.connect("GET",
                                                         self.session.api_host,
                                                         path, headers=headers,
                                                         params=params)
            disposition, exc = self.response_disposition(status_code, path,
                                                         reason)
            if disposition == "rekey":
                print("Session token bad: %s" % self.session.api_token)
                self.session.authenticate()
                print("Session token refreshed: %s" % self.session.api_token)
                tries += 1
                continue
            elif disposition == "wait":
                time.sleep(5)
                tries += 1
                continue
            elif disposition == "bad":
                raise exc
            elif disposition == "good":
                break
        if exc:
            raise exc  # This catches the fails beyond retries.
        return json.loads(body)

    @classmethod
    def response_disposition(cls, response_code, url, resp_text):
        """Return either "good", "bad", "rekey", or "wait"."""
        disposition = "bad"  # Fails if unmatched.
        exc = CloudPassageGeneral(resp_text)
        bad_statuses = {400: CloudPassageValidation(resp_text, code=400),
                        404: CloudPassageResourceExistence(resp_text, code=404,
                                                           url=url),
                        403: CloudPassageAuthorization(resp_text, code=403),
                        422: CloudPassageValidation(resp_text, code=422)}
        if 200 <= response_code < 300:
            disposition = "good"
            exc = None
        elif response_code == 401:
            disposition = "rekey"
        elif 400 <= response_code < 500:
            disposition = "bad"
            try:
                exc = bad_statuses[response_code]
            except KeyError:
                # If we don't have a specific exc, leave it CloudPassageGeneral
                pass
        elif 500 <= response_code <= 599:
            disposition = "wait"
        return disposition, exc

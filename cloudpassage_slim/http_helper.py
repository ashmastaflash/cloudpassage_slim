import base64
import urllib2


class HttpHelper(object):
    """Instantiate this class with a HaloSession object."""
    def __init__(self, session):
        self.session = session

    def delete(self, url, **kwargs):
        if "params" in kwargs:
            params = kwargs["params"]
        else:
            params = None
        return

    def get(self, url):
        return

    def post(self, url):
        return

    def put(self, url):
        return

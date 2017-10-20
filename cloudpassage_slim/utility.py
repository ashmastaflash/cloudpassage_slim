from exceptions.Exceptions import CloudPassageAuthentication
from exceptions.Exceptions import CloudPassageAuthorization
from exceptions.Exceptions import CloudPassageGeneral
from exceptions.Exceptions import CloudPassageResourceExistence
from exceptions.Exceptions import CloudPassageValidation


class Utility(object):
    def parse_status(url, resp_code, resp_text):
        """Parse status from HTTP response"""
        success = True
        exc = None
        if resp_code not in [200, 201, 202, 204]:
            success = False
            bad_statuses = {400: CloudPassageValidation(resp_text, code=400),
                            401: CloudPassageAuthentication(resp_text,
                                                            code=401),
                            404: CloudPassageResourceExistence(resp_text,
                                                               code=404,
                                                               url=url),
                            403: CloudPassageAuthorization(resp_text,
                                                           code=403),
                            422: CloudPassageValidation(resp_text, code=422)}
            if resp_code in bad_statuses:
                return(success, bad_statuses[resp_code])
            else:
                return(success, CloudPassageGeneral(resp_text, code=resp_code))
        return success, exc

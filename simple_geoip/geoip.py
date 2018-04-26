"""
simple_geoip.geoip
~~~~~~~~~~~~~~~~~~

The module holds the main simple-geoip library implementation.
"""


from backoff import expo, on_exception
from requests import get
from requests.exceptions import RequestException

from .exceptions import ConnectionError, ServiceError
from .settings import API_URI, MAX_RETRIES, USER_AGENT


class GeoIP:

    def __init__(self, api_key):
        self.api_key = api_key
        self.verify()

    def verify(self):
        """
        Verify configuration parameters are valid.

        :raises: ValueError if configuration data is invalid.
        """
        if not self.api_key:
            raise ValueError("api_key is required")

        if not isinstance(self.api_key, str):
            raise ValueError("api_key must be a string")

    def lookup(self, ip):
        """
        Look up geographical information for an IP address using the
        geoipify.whoisxmlapi.com service.

        :param str ip: The IP address to geolocate.
        :rtype: dict
        :returns: A dict containing IP geolocation information.
        :raises: GeoIPError if something bad happens.
        """
        try:
            resp = _get_resp(self.api_key, ip)
        except RequestException:
            raise ConnectionError("The request failed because it wasn't able to reach the GeoIPify service. This is most likely due to a networking error of some sort.")

        if resp.status_code != 200:
            raise ServiceError('Received an invalid status code from GeoIPify:' + str(resp.status_code) + '. The service might be experiencing issues.')

        return resp.json()



@on_exception(expo, RequestException, max_tries=MAX_RETRIES)
def _get_resp(api_key, ip):
    """
    Internal function which attempts to geolocate an IP address via the
    GeoIPify service (https://geoipify.whoisxmlapi.com/).

    :param str api_key: The API key to authenticate with.
    :rtype: obj
    :returns: The response object from the HTTP request.
    :raises: RequestException if something bad happened and the request wasn't
        completed.

    .. note::
        If an error occurs when making the HTTP request, it will be retried
        using an exponential backoff algorithm.  This is a safe way to retry
        failed requests without giving up.
    """
    return get(API_URI,
        headers={'user-agent': USER_AGENT},
        params={'apiKey': api_key, 'ipAddress': ip}
    )

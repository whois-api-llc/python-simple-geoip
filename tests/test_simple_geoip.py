"""
tests.simple_geoip.geoip
~~~~~~~~~~~~~~~~~~~~~~~~

All tests for our simple_geoip.geoip module.
"""


from os import environ
from unittest import TestCase

from requests.models import Response

from simple_geoip.exceptions import ConnectionError, GeoIPException, ServiceError
from simple_geoip.geoip import _get_resp


class BaseTest(TestCase):
    """A base test class."""

    def setUp(self):
        import simple_geoip
        self._api_uri = simple_geoip.settings.API_URI

    def tearDown(self):
        import simple_geoip
        simple_geoip.settings.API_URI = self._api_uri


class GetRespTest(BaseTest):
    """Tests for our helper function: ``_get_resp``."""

    def test_returns_response(self):
        self.assertIsInstance(_get_resp('test', 'test'), Response)


class GeoIPLookupTest(BaseTest):
    """Tests for our ``GeoIP.lookup()`` method."""

    def test_raises_connection_error_on_connection_error(self):
        import simple_geoip

        simple_geoip.geoip.API_URI = 'https://api.asdgasggasgdasgdsasgdasdfadfsda.com'
        geoip = simple_geoip.GeoIP('test')

        self.assertRaises(ConnectionError, geoip.lookup, '8.8.8.8')

    def test_raises_geoip_exception_on_error(self):
        import simple_geoip

        simple_geoip.geoip.API_URI = 'https://api.asdgasggasgdasgdsasgdasdfadfsds.com'
        geoip = simple_geoip.GeoIP('test')

        self.assertRaises(GeoIPException, geoip.lookup, '8.8.8.8')

    def test_raises_service_error_on_error(self):
        import simple_geoip

        simple_geoip.geoip.API_URI = 'https://api.ipify.org/woo'
        geoip = simple_geoip.GeoIP('test')

        self.assertRaises(ServiceError, geoip.lookup, '8.8.8.8')

    def test_returns_geoip_data(self):
        import simple_geoip

        simple_geoip.geoip.API_URI = 'https://geoipify.whoisxmlapi.com/api/v1'
        geoip = simple_geoip.GeoIP(environ.get('API_KEY'))

        self.assertEquals(geoip.lookup('8.8.8.8')['ip'], '8.8.8.8')

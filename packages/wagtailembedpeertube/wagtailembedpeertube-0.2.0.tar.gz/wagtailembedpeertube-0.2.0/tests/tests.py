from unittest.mock import patch

from django.test import TestCase

from wagtailembedpeertube.finders import PeertubeFinder

PEERTUBE_URL = (
    'https://framatube.org/videos/watch/9c9de5e8-0a1e-484a-b099-e80766180a6d'
)


class TestPeertubeFinder(TestCase):
    def setUp(self):
        self.finder = PeertubeFinder()

        class DummyResponse:
            def read(self):
                return b'foo'

        self.dummy_response = DummyResponse()

    def test_accepts_peertube(self):
        self.assertTrue(self.finder.accept(PEERTUBE_URL))

    def test_doesnt_accept_other_provider(self):
        self.assertFalse(self.finder.accept('http://www.youtube.com/watch/'))

    @patch('urllib.request.urlopen')
    @patch('json.loads')
    def test_endpoint_return_value(self, loads, urlopen):
        urlopen.return_value = self.dummy_response
        loads.return_value = {
            'type': 'something',
            'url': 'http://www.example.com',
            'title': 'test_title',
            'author_name': 'test_author',
            'provider_name': 'test_provider_name',
            'thumbnail_url': 'test_thumbail_url',
            'width': 'test_width',
            'height': 'test_height',
            'html': 'test_html',
        }

        result = self.finder.find_embed(PEERTUBE_URL)

        endpoint_url = urlopen.call_args[0][0].full_url
        self.assertTrue(
            endpoint_url.startswith('https://framatube.org/services/oembed?'),
            "{} doesn't start with expected endpoint".format(endpoint_url),
        )

        self.assertEqual(
            result,
            {
                'type': 'something',
                'title': 'test_title',
                'author_name': 'test_author',
                'provider_name': 'test_provider_name',
                'thumbnail_url': 'test_thumbail_url',
                'width': 'test_width',
                'height': 'test_height',
                'html': 'test_html',
            },
        )

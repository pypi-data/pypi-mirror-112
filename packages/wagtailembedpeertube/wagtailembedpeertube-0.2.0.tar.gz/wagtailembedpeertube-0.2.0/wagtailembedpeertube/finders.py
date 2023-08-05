# wagtailembedpeertube - Embed PeerTube videos into Wagtail
# Copyright (C) 2018  Cliss XXI <tech@cliss21.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import re

from wagtail.embeds.finders.oembed import OEmbedFinder

PEERTUBE_URL_PATH_RE = re.compile(
    r'^/videos/watch/[0-9a-fA-F]{8}(-[0-9a-fA-F]{4}){3}-[0-9a-fA-F]{12}$'
)


class PeertubeFinder(OEmbedFinder):
    PEERTUBE_ENDPOINT_PATH = '/services/oembed'
    PEERTUBE_URL_PATTERNS = [
        (
            r'^(https?://[^/]+)/videos/watch/'
            r'[0-9a-fA-F]{8}(-[0-9a-fA-F]{4}){3}-[0-9a-fA-F]{12}$'
        )
    ]

    def __init__(self):
        self._patterns = [
            re.compile(url) for url in self.PEERTUBE_URL_PATTERNS
        ]

    def _get_endpoint(self, url):
        for pattern in self._patterns:
            m = pattern.match(url)
            if m is not None:
                return m.group(1) + self.PEERTUBE_ENDPOINT_PATH


embed_finder_class = PeertubeFinder

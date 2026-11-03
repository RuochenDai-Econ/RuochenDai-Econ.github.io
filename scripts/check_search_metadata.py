"""Check generated page identities against the sitemap before publication."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://ruochendai-econ.github.io'
PAGES = {'index.html': '/', 'research/index.html': '/research/',
         'research/chinese/index.html': '/research/chinese/',
         'research/working-papers/index.html': '/research/working-papers/'}

class SearchMetadata(HTMLParser):
    def __init__(self):
        super().__init__()
        self.canonical = []
        self.social_url = []
        self.robots = []

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if tag == 'link' and attrs.get('rel') == 'canonical':
            self.canonical.append(attrs.get('href'))
        if tag == 'meta' and attrs.get('property') == 'og:url':
            self.social_url.append(attrs.get('content'))
        if tag == 'meta' and attrs.get('name', '').lower() in ('robots', 'googlebot'):
            self.robots.append(attrs.get('content', '').lower())

sitemap = ET.parse(ROOT / 'sitemap.xml')
listed_urls = {element.text for element in sitemap.iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')}
for filename, path in PAGES.items():
    expected = BASE + path
    metadata = SearchMetadata()
    metadata.feed((ROOT / filename).read_text())
    assert metadata.canonical == [expected], (filename, metadata.canonical)
    assert metadata.social_url == [expected], (filename, metadata.social_url)
    assert expected in listed_urls, filename
    assert urlsplit(expected).hostname == 'ruochendai-econ.github.io'
    assert all('noindex' not in directive and 'none' not in directive for directive in metadata.robots)
    print(filename + ': ' + expected)
print('PASS: all four pages identify themselves correctly and agree with the sitemap.')

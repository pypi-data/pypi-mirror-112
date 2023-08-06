from .adapters.http_client import HttpClient
from .pipeline.html_parser import HtmlParser
from .pipeline.sanitizer import Sanitizer
from .pipeline.transformer import Transformer

class HDistill():

    def __init__(self, HttpClient, HtmlParser, Sanitizer, Transformer):
        self._http_client = HttpClient
        self._html_parser = HtmlParser
        self._sanitizer = Sanitizer
        self._transformer = Transformer

    def distill(self, url: str, xpath: str) -> []:
        html_content = self._http_client.get_html_content(url)
        parsed = self._html_parser.parse_html(html_content, xpath)
        sanitized = self._sanitizer.sanitize(parsed)
        return self._transformer.transform(sanitized)

class EtlHandler():

    def process(self, url: str, xpath: str):
        pass

class RawConsoleHandler(EtlHandler):

    def __init__(self, HttpClient, HtmlParser, Sanitizer, ConsoleLoader):
        self._http_client = HttpClient
        self._html_parser = HtmlParser
        self._sanitizer = Sanitizer
        self._loader = ConsoleLoader

    def process(self, url: str, xpath: str):
        html_content = self._http_client.get_html_content(url)
        parsed = self._html_parser.parse_html(html_content, xpath)
        sanitized = self._sanitizer.sanitize(parsed)
        self._loader.load(sanitized)

class TransformConsoleHandler(EtlHandler):

    def __init__(self, HttpClient, HtmlParser, Sanitizer, Transformer, ConsoleLoader):
        self._http_client = HttpClient
        self._html_parser = HtmlParser
        self._sanitizer = Sanitizer
        self._transformer = Transformer
        self._loader = ConsoleLoader

    def process(self, url: str, xpath: str):
        html_content = self._http_client.get_html_content(url)
        parsed = self._html_parser.parse_html(html_content, xpath)
        sanitized = self._sanitizer.sanitize(parsed)
        transformed = self._transformer.transform(sanitized)
        self._loader.load(transformed)

class RawJsonHandler(EtlHandler):

    def __init__(self, HttpClient, HtmlParser, Sanitizer, JsonLoader):
        self._http_client = HttpClient
        self._html_parser = HtmlParser
        self._sanitizer = Sanitizer
        self._loader = JsonLoader

    def process(self, url: str, xpath: str):
        html_content = self._http_client.get_html_content(url)
        parsed = self._html_parser.parse_html(html_content, xpath)
        sanitized = self._sanitizer.sanitize(parsed)
        self._loader.load(sanitized)

class TransformJsonHandler(EtlHandler):

    def __init__(self, HttpClient, HtmlParser, Sanitizer, Transformer, JsonLoader):
        self._http_client = HttpClient
        self._html_parser = HtmlParser
        self._sanitizer = Sanitizer
        self._transformer = Transformer
        self._loader = JsonLoader

    def process(self, url: str, xpath: str):
        html_content = self._http_client.get_html_content(url)
        parsed = self._html_parser.parse_html(html_content, xpath)
        sanitized = self._sanitizer.sanitize(parsed)
        transformed = self._transformer.transform(sanitized)
        self._loader.load(transformed)


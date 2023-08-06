import urllib.request

class HttpClient():

    def get_html_content(self, url: str) -> str:
        return urllib.request.urlopen(url).read()

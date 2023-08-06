from lxml import html

class HtmlParser():

    def parse_html(self, input: str, xpath: str) -> []:
        """
        Parses the input HTML based on the provided xpath query
        
        Returns a list of strings containing the parsed elements
        """
        tree = html.fromstring(input)
        return tree.xpath(xpath)
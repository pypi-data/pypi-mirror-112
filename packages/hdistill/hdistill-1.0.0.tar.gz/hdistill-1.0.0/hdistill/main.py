from .adapters.http_client import HttpClient
from .pipeline.html_parser import HtmlParser
from .pipeline.sanitizer import Sanitizer
from .pipeline.transformer import Transformer
from .command_handler import get_command_handler
import pprint
import argparse
import sys

class SplitArgs(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values.split(','))

def main():
    args = parse_args()
    handler = get_command_handler(args)
    handler.process(args.url, args.xpath)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="the URL of a webpage")
    parser.add_argument("xpath", help="the XPath query to extract specific data from the source HTML")
    parser.add_argument("-t", "--transform", dest="keys", action=SplitArgs, type=str, default=None,
                        help="a list of keys to map the parsed output to. Keys must be provided as a comma-separated string. The number of keys determines the size of the sub-lists that the raw parsed output is split into, before being formed into a map")
    parser.add_argument("-o", "--output", dest="output", action="store", default=None,
                        help="the destination file name for the output. If the file exists it will be overwritten. Output is in JSON and .json will be appended to the file name")
    return parser.parse_args()

if __name__ == "__main__":
    main()
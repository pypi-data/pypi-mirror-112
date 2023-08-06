from adapters.http_client import HttpClient
from pipeline.html_parser import HtmlParser
from pipeline.sanitizer import Sanitizer
from pipeline.transformer import Transformer
import hdistill
import pprint
import argparse
import sys

class SplitArgs(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values.split(','))

def main():
    sys.path.append(".")
    args = parse_args()
    process(args)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="the URL of a webpage")
    parser.add_argument("xpath", help="the XPath query to extract specific data from the source HTML")
    parser.add_argument("set_size", help="used to transform a list of parsed HTML data into sublists of the given set_size", type=int)
    parser.add_argument("keys", help="a comma separated list of keys used as labels for each element in a set", action=SplitArgs)
    return parser.parse_args()

def process(args):
    http_client = HttpClient()
    html_parser = HtmlParser()
    sanitizer = Sanitizer()
    transformer = Transformer(
        args.set_size,
        args.keys)
    hdistill = HDistill(http_client, html_parser, sanitizer, transformer)
    distilled = hdistill.distill(args.url, args.xpath)
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(distilled)

if __name__ == "__main__":
    main()
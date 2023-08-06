from .pipeline.handlers import *
from .adapters.http_client import HttpClient
from .pipeline.html_parser import HtmlParser
from .pipeline.sanitizer import Sanitizer
from .pipeline.transformer import Transformer
from .pipeline.loader import *
import pprint

def get_command_handler(args):
    if args.keys is None and args.output is None:
        return RawConsoleHandler(HttpClient(), HtmlParser(), Sanitizer(), ConsoleLoader(pprint.PrettyPrinter(indent=4)))
    if args.keys is None and args.output is not None:
        return RawJsonHandler(HttpClient(), HtmlParser(), Sanitizer(), JsonLoader(args.output))
    if args.keys is not None and args.output is None:
        return TransformConsoleHandler(HttpClient(), HtmlParser(), Sanitizer(), Transformer(args.keys), ConsoleLoader(pprint.PrettyPrinter(indent=4)))
    if args.keys is not None and args.output is not None:
        return TransformJsonHandler(HttpClient(), HtmlParser(), Sanitizer(), Transformer(args.keys), JsonLoader(args.output))
        
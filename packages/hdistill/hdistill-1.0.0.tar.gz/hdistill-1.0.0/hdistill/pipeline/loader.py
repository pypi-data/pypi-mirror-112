import json

class Loader():

    def load(self, data: []) -> None:
        pass

class ConsoleLoader(Loader):

    def __init__(self, PPrinter):
        self._pprinter = PPrinter

    def load(self, data: []):
        self._pprinter.pprint(data)

class JsonLoader(Loader):

    def __init__(self, output_file: str):
        self._output_file = output_file

    def load(self, data: []):
        with open(f'{self._output_file}.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

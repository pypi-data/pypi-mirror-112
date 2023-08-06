class Transformer():

    def __init__(self, keys: []):
        self._keys = keys
        self._transformed = []

    def transform(self, input: []) -> []:
        grouped_sets = self.__split_sets_by_set_size(input)
        transformed = []
        for set in grouped_sets:
            transformed_set = {}
            for i in range(0, len(set)):
                transformed_set[self._keys[i]] = set[i]
            transformed.append(transformed_set)
        return transformed

    def __split_sets_by_set_size(self, input: []) -> []:
        return [input[x: x + len(self._keys)] for x in range(0, len(input), len(self._keys))]

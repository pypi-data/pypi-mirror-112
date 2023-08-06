import unittest
from hdistill.pipeline.transformer import Transformer

class TransformerTests(unittest.TestCase):

    def test_sanitizer_strips_whitespace_and_newlines(self):
        transformer = Transformer(['Rank', 'Key People', 'Title', 'Year Released'])
        actual_output = transformer.transform(input)
        self.assertEqual(expected_output, actual_output)

input = ['1.', 'Frank Darabont (dir.), Tim Robbins, Morgan Freeman', 'The Shawshank Redemption', '(1994)',]
expected_output = [
    {
        'Rank': '1.',
        'Key People': 'Frank Darabont (dir.), Tim Robbins, Morgan Freeman',
        'Title': 'The Shawshank Redemption',
        'Year Released': '(1994)'
    }
]
import unittest
from hdistill.pipeline.sanitizer import Sanitizer

class SanitizerTests(unittest.TestCase):

    def test_sanitizer_strips_whitespace_and_newlines(self):
        sanitizer = Sanitizer()
        actual_output = sanitizer.sanitize(input)
        self.assertEqual(expected_output, actual_output)


input = ['\n      1.\n      ', 'Frank Darabont (dir.), Tim Robbins, Morgan Freeman', 'The Shawshank Redemption', '\n        ', '(1994)', '\n    ']
expected_output = ['1.', 'Frank Darabont (dir.), Tim Robbins, Morgan Freeman', 'The Shawshank Redemption', '(1994)',]
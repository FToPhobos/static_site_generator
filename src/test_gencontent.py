import unittest
from gencontent import extract_title

class TestGenContent(unittest.TestCase):
    def test_extract_title(self):
        md = "# Hello"
        result = extract_title(md)
        self.assertEqual(result, "Hello")

    def test_extract_title_ml(self):
        md ="dqsfdsqfqdfqsdqs\n# Hello there\nsqdsqdsq"
        result = extract_title(md)
        self.assertEqual(result, "Hello there")
import unittest
import logging
from dogemachine_utils import text_parser_utils

logger = logging.getLogger(__name__)


class TextParserUtilsTestCase(unittest.TestCase):
    def test_parse_text_for_url(self):
        # Case: Base URL
        some_args = f"-u 'http://testphp.vulnweb.com' --crawl -l 3 --params --blind --skip"
        result = text_parser_utils.parse_text_for_url(string=some_args)
        self.assertEqual(result, "http://testphp.vulnweb.com")
        # Case: /sup.html
        some_args = f"-u 'http://testphp.vulnweb.com/sup.html' --crawl -l 3 --params --blind --skip"
        result = text_parser_utils.parse_text_for_url(string=some_args)
        self.assertEqual(result, "http://testphp.vulnweb.com/sup.html")
        # Case: With query parameters
        some_args = f"-u 'http://testphp.vulnweb.com/sup.html?bruh' --crawl -l 3 --params --blind --skip"
        result = text_parser_utils.parse_text_for_url(string=some_args)
        self.assertEqual(result, "http://testphp.vulnweb.com/sup.html?bruh")

    def test_clean_url_string_for_s3_object_name(self):
        url_string = "http://testphp.vulnweb.com/sup.html"
        result = text_parser_utils.clean_url_string_for_s3_object_name(url_string=url_string)
        print(result)

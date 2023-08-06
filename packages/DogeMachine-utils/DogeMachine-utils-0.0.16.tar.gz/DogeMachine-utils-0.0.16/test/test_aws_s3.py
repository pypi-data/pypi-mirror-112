import unittest
from dogemachine_utils.aws_s3_utils import get_report_object_key_path

"""
I think we are mostly interested in the URL, then the tool.
# The URL can be weird. Maybe we want:

The user cares about things in this order:
1. "The website/endpoint I scanned" - aka What is the URL?
2. "The vulnerability that I targeted" - this is specific to each scan, i.e., RXSS etc.
3. "When I scanned" - i.e., the timestamp
4. "The tool itself" - whether it is ZAP, XSS, etc. This is actually the lowest priority.

In terms of formatting, the weirdest thing to make uniform is the website/endpoint I scanned. 
If we allow /, then it could be near infinite levels deep.
But if we just make them all unique, the root level of the bucket could be way too much to scroll through.
Thinking about this from a consulting perspective, if I was using this for consulting, I'd want:
* The root of the bucket to be tld.com
* The second level to be subdomain.tld.com
* The third level to be the URL path (for subdomain.tld.com/pages/, this would be `pages` - only if the scan specifically targeted that path, though). Subsequent / would be normalized to + characters

* That allows me to categorize my clients very cleanly without making subdomain-heavy clients to clutter the root level
* Then the URL path allows me to categorize sections, and even though that might get cluttered, it's pretty acceptable.


"""


class AwsS3TestCase(unittest.TestCase):

    def test_get_report_path_case_0(self):
        """Case 0: TLD with no subdomain"""
        url = "http://vulnweb.com"
        result = get_report_object_key_path(
            url=url, tool_name="zap", scan_name="rxss", date_string="2021-06-06",
            time_string="1023Z", file_extension="xml"
        )
        print(result)
        expected_result = "vulnweb.com/vulnweb.com/root/rxss/2021-06-06/zap/1023Z.xml"
        self.assertEqual(result, expected_result)

    def test_get_report_path_case_1(self):
        """Case 1: TLD with subdomain and URL path"""
        url = "http://testphp.vulnweb.com"
        result = get_report_object_key_path(
            url=url, tool_name="zap", scan_name="rxss", date_string="2021-06-06",
            time_string="1023Z", file_extension="xml"
        )
        print(result)
        expected_result = "vulnweb.com/testphp.vulnweb.com/root/rxss/2021-06-06/zap/1023Z.xml"
        self.assertEqual(result, expected_result)

    def test_get_report_path_case_2(self):
        """Case 2: TLD with subdomain, path"""
        url = "http://testphp.vulnweb.com/sup/"
        result = get_report_object_key_path(
            url=url, tool_name="zap", scan_name="rxss", date_string="2021-06-06",
            time_string="1023Z", file_extension="xml"
        )
        expected_result = "vulnweb.com/testphp.vulnweb.com/sup/rxss/2021-06-06/zap/1023Z.xml"
        print(result)
        self.assertEqual(result, expected_result)

    def test_get_report_path_case_3(self):
        """Case 3: TLD with subdomain and nested path levels"""
        url = "http://testphp.vulnweb.com/sup/bruh/yolo/"
        result = get_report_object_key_path(
            url=url, tool_name="zap", scan_name="rxss", date_string="2021-06-06",
            time_string="1023Z", file_extension="xml"
        )
        expected_result = "vulnweb.com/testphp.vulnweb.com/sup+bruh+yolo/rxss/2021-06-06/zap/1023Z.xml"
        print(result)
        self.assertEqual(result, expected_result)

    def test_get_report_path_case_4(self):
        """Case 4: TLD with subdomain, path, and query string"""
        url = "http://testphp.vulnweb.com/sup/bruh/yolo?question=why"
        result = get_report_object_key_path(
            url=url, tool_name="zap", scan_name="rxss", date_string="2021-06-06",
            time_string="1023Z", file_extension="xml"
        )
        print(result)
        # TODO: Right now the query string is not included here. Maybe we change that, idk.
        expected_result = "vulnweb.com/testphp.vulnweb.com/sup+bruh+yolo/rxss/2021-06-06/zap/1023Z.xml"
        self.assertEqual(result, expected_result)

    def test_get_report_path_several(self):
        """Case N: Try several different URLs and make sure it doesn't throw errors"""
        urls = [
            "https://testasp.vulnweb.com/",
            "https://testaspnet.vulnweb.com/",
            "https://testphp.vulnweb.com/",
            "http://crackme.cenzic.com/",
            "http://zero.webappsecurity.com/",
            "http://demo.testfire.net/",
            "http://aspnet.testsparker.com/",
            "http://php.testsparker.com/",
            "http://www.webscantest.com/",
            "http://escape.alf.nu/",
            "http://google-gruyere.appspot.com/",
            "http://www.hackthissite.org/",
            "https://defendtheweb.net/?hackthis",
            "https://hack.me",
            "https://xss-game.appspot.com/",
            "http://xss.progphp.com/",
            "http://pwnable.tw/",
            "http://pwnable.kr/",
            "https://juice-shop.herokuapp.com/#/"
        ]
        for url in urls:
            result = get_report_object_key_path(
                url=url, tool_name="zap", scan_name="rxss", date_string="2021-06-06",
                time_string="1023Z", file_extension="xml"
            )
            print(result)

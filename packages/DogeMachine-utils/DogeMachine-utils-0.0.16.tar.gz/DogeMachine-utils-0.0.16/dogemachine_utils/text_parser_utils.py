import re


def parse_text_for_url(string: str) -> str:
    return re.search("(?P<url>https?://[^\s'\"]+)", string).group("url")


def clean_url_string_for_s3_object_name(url_string: str) -> str:
    """Given a URL, return a string that can be used as a single folder name in AWS S3 object key. See unit test for examples."""
    result = url_string.replace("http://", "").replace("https://", "").replace("/", "+")
    return result

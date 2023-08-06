import logging
import boto3
from dogemachine_utils.time_utils import get_year_month_day_string, get_current_time_string
from dogemachine_utils.file_utils import read_file
from urllib.parse import urlparse
import time
from dogemachine_utils import time_utils
from dogemachine_utils.text_parser_utils import parse_text_for_url
from dogemachine_utils.aws_lambda_utils import is_running_in_aws_lambda, is_running_in_sam_cli_local
from dogemachine_utils.aws_login import get_boto3_client, get_current_account_id

logger = logging.getLogger(__name__)


def get_doge_machine_bucket_name(profile: str = None) -> str:
    """Get the standard name of the Doge Machine bucket"""
    account_id = get_current_account_id(profile=profile)
    name = f"doge-machine-results-{account_id}"
    return name


def get_tld(url: str) -> str:
    o = urlparse(url)
    tld = ".".join(o.netloc.split(".")[-2:])
    return tld


def get_tld_with_subdomain(url: str) -> str:
    o = urlparse(url)
    tld_with_subdomain = o.netloc
    return tld_with_subdomain


def get_url_path(url: str) -> str:
    o = urlparse(url)
    if o.path:
        url_path = o.path
        if url_path == "/":
            url_path = "root"
        # if it starts with /, remove that
        if url_path[0] == "/":
            url_path = url_path[1:]
        if url_path[-1] == "/":
            url_path = url_path[:-1]
        url_path = url_path.replace("/", "+")  # this includes URL query strings, if the report is specific to that
    else:
        url_path = "root"
    return url_path


def get_report_object_key_path(url: str, scan_name: str, tool_name: str, date_string: str = None, time_string: str = None,
                               file_extension: str = "txt"):
    """
    Return the S3 object key to use for the report.

    :param url: The URL for the scan
    :param scan_name: The name of the scan, usually corresponding to the finding you are targeting, like rxss, etc.
    :param tool_name: The name of the tool, like zap, xsstrike, dalfox, nmap, sqlmap
    :param date_string: Like 2012-03-17
    :param time_string: Like "%H%MZ"
    :param file_extension: Like xml, json, pdf, html
    """
    if not date_string:
        date_string = time_utils.get_year_month_day_string()
    if not time_string:
        time_string = time_utils.get_current_time_z_string()
    tld = get_tld(url=url)
    tld_with_subdomain = get_tld_with_subdomain(url=url)
    url_path = get_url_path(url=url)
    url_object_component = f"{tld}/{tld_with_subdomain}/{url_path}"
    # Timestamp approach: https://serverfault.com/questions/292014/preferred-format-of-file-names-which-include-a-timestamp#answer-370766
    # 2012-03-17T1748Z
    object_key = f"{url_object_component}/" \
                 f"{scan_name}/" \
                 f"{date_string}/" \
                 f"{tool_name}/" \
                 f"{time_string}.{file_extension}"
    return object_key


def get_object_from_s3(bucket_name: str, object_key: str, s3_client: boto3.Session.client):
    """Get object contents from  S3"""
    logger.info(f"Downloading object: s3://{bucket_name}/{object_key}")
    response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
    content = response['Body'].read().decode('utf-8')
    return content


def write_simple_object_to_s3(content: str, bucket_name: str, object_key: str, s3_client: boto3.Session.client) -> dict:
    """Write an object to S3 with basic AES256 encryption"""
    logger.info(f"Writing object: s3://{bucket_name}/{object_key}")
    response = s3_client.put_object(
        ACL="private",
        Bucket=bucket_name,
        Key=object_key,
        ServerSideEncryption="AES256",
        Body=content
    )
    logger.debug(response)
    return response


def save_results_file_to_s3_from_aws_lambda(
        results_file: str,
        results_object_key: str,
        bucket: str,
        profile: str = None,
        save_anyway: bool = False,
) -> dict:
    """
    If it's running in AWS Lambda, save the file contents to S3

    :param bucket: The bucket name
    :param results_object_key: The path to the results in S3
    :param results_file: Path to the results file to save to S3
    :param profile: AWS Profile name
    :param save_anyway: If set to true, it will save to S3 anyway, even if it is not inside SAM CLI or in AWS Lambda
    :return:
    """
    contents = read_file(results_file)

    # TODO: Get a good naming convention going for this. I want to be able to save the results to a file name that I want, I think. And a format of my choice.
    def save_results():
        logger.info("Saving to S3...")
        logger.info(f"Will save to: s3://{bucket}/{results_object_key}")
        s3_client = get_boto3_client(service="s3", region="us-east-1", profile=profile)
        response = write_simple_object_to_s3(
            content=contents,
            bucket_name=bucket,
            object_key=results_object_key,
            s3_client=s3_client
        )
        return response

    if not is_running_in_sam_cli_local() and is_running_in_aws_lambda():
        return save_results()
    elif save_anyway:
        return save_results()
    else:
        return {}

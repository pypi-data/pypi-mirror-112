"""AWS Login utilities"""
import os
import logging
import boto3
from botocore.config import Config
logger = logging.getLogger(__name__)


def get_boto3_client(service: str, profile: str = None, region="us-east-1") -> boto3.Session.client:
    """Get a boto3 client for a given service"""
    logging.getLogger('botocore').setLevel(logging.CRITICAL)
    session_data = {"region_name": region}
    if profile:
        session_data["profile_name"] = profile
    session = boto3.Session(**session_data)

    config = Config(connect_timeout=5, retries={"max_attempts": 10})
    if os.environ.get('LOCALSTACK_ENDPOINT_URL'):
        client = session.client(service, config=config, endpoint_url=os.environ.get('LOCALSTACK_ENDPOINT_URL'))
    else:
        client = session.client(service, config=config, endpoint_url=os.environ.get('LOCALSTACK_ENDPOINT_URL'))
    logger.debug(f"{client.meta.endpoint_url} in {client.meta.region_name}: boto3 client login successful")
    return client


def get_current_account_id(profile: str = None) -> str:
    """Get the current account ID"""
    sts_client = get_boto3_client(service="sts", profile=profile, region="us-east-1")
    response = sts_client.get_caller_identity()
    current_account_id = response.get("Account")
    return current_account_id
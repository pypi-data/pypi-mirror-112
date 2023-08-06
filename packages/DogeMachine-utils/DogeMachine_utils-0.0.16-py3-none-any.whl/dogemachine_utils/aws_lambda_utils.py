import os


def is_running_in_aws_lambda() -> bool:
    """Detects if running in AWS Lambda"""
    return os.environ.get("LAMBDA_TASK_ROOT") is not None and os.environ.get("AWS_EXECUTION_ENV") is not None


def is_running_in_sam_cli_local() -> bool:
    """Detects if running in AWS SAM locally"""
    return os.environ.get("AWS_SAM_LOCAL") is not None

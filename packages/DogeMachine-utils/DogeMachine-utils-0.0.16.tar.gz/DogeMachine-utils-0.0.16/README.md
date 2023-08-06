# DogeMachine-utils

This package contains helper methods and common tasks used by the various Lambda functions deployed by [DogeMachine](https://github.com/kmcquade/DogeMachine).

[https://github.com/kmcquade/DogeMachine-utils](https://github.com/kmcquade/DogeMachine-utils)

[![Downloads](https://pepy.tech/badge/DogeMachine-utils)](https://pepy.tech/project/DogeMachine-utils)

# Helper functions

For example:

* Saving the object to S3, and formatting the save object easily
* Checking if we are running in a Lambda function, in SAM CLI, etc.
* Various functions that are currently in [kinnaird-utils](https://pypi.org/project/kinnaird-utils/)

# Naming Convention methods

## S3 Bucket Naming Convention

The method `dogemachine_utils.aws_s3.get_doge_machine_bucket_name` will return an S3 Bucket with the name `doge-machine-results-111222333` where the AWS account number is `1111222333`.

## S3 Object Naming Convention for scan results

The method `dogemachine_utils.aws_s3.get_report_object_key_path` will return an object key path based on the supplied `tool_name`, `target_url_string`, and `report_name`.


# References

* [DogeMachine](https://github.com/kmcquade/DogeMachine)


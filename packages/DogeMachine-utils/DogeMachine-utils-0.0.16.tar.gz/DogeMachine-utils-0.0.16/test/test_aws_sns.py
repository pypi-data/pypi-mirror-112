import unittest
import json
from dogemachine_utils import aws_sns_utils


class AwsSnsTestCase(unittest.TestCase):
    def test_translate_dict_to_message_attributes(self):
        example = {
            "scan_name": "rxss",
            "attack_strength": "Medium",
            "alert_threshold": "Medium",
            "active_scan_rule_ids": "40019",
            "target_url": "https://test.vulnweb.com",
            "bucket": "doge-machine-results-111122223333"
        }
        results = aws_sns_utils.translate_dict_to_message_attributes(kv_pair=example)
        print(json.dumps(results, indent=4))
        expected_results = {
            "scan_name": {
                "DataType": "String",
                "StringValue": "rxss"
            },
            "attack_strength": {
                "DataType": "String",
                "StringValue": "Medium"
            },
            "alert_threshold": {
                "DataType": "String",
                "StringValue": "Medium"
            },
            "active_scan_rule_ids": {
                "DataType": "String",
                "StringValue": "40019"
            },
            "target_url": {
                "DataType": "String",
                "StringValue": "https://test.vulnweb.com"
            },
            "bucket": {
                "DataType": "String",
                "StringValue": "doge-machine-results-111122223333"
            }
        }
        self.assertDictEqual(results, expected_results)

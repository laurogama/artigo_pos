from datetime import datetime
from random import randint
from unittest import TestCase

from message_handler import verify_fields

__author__ = 'laurogama'


class TestVerify_fields(TestCase):
    def test_ok_message(self):
        mock_message = {
            "id": randint(1, 1000),
            "timestamp": str(datetime.now()),
            "data": {
                "temperature": randint(1, 100),
                "humidity": randint(1, 300),
                "luminance": randint(1, 300),
                "noise": randint(1, 300),
                "carbon_monoxide": randint(1, 300),
            }
        }
        self.assertTrue(verify_fields(mock_message))

    def test_ko_message(self):
        mock_message = {
            "id": randint(1, 1000),
            "data": {
                "temperature": randint(1, 100),
                "humidity": randint(1, 300),
                "luminance": randint(1, 300),
                "noise": randint(1, 300),
                "carbon_monoxide": randint(1, 300),
            }
        }
        self.assertFalse(verify_fields(mock_message))

"""
This module contains our apps errors
"""


class Unauthorized(Exception):
    def __init__(self, message: str):
        self.message = message


class TokenExpired(Exception):
    def __init__(self, next_url: str):
        self.next_url = next_url


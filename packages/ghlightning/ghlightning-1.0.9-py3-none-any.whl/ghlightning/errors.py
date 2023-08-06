#!/usr/bin/python3

class Errors(Exception):
    pass


class UsernameNotFound(Errors):
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)


class OrganizationAccount(Errors):
    def __init__(self, message):
        super().__init__(message)



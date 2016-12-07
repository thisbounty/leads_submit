import os

def values():
    return {
        'username': os.environ['freelance_username'],
        'password': os.environ['freelance_password'],
    }

def rest_values():
    return {
        'endpoint': os.environ['leads_read_url'],
    }

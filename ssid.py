import random
import time

def create_UUID():
    dt = int((time.time() * 1000) % (2**32))  # Get current time in milliseconds
    uuid_template = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'
    uuid = ''.join(c if c != 'x' else random.choice('0123456789abcdef') for c in uuid_template)
    return uuid

# Example usage


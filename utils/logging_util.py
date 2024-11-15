import json

def log_event(message, data):
    print(f"{message} {json.dumps(data)}")

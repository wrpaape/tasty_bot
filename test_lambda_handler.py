#!/usr/bin/env python
import json

from lambda_handler import lambda_handler, inspect_json

EVENT_PATH = 'test_event.json'


if __name__ == '__main__':
    with open(EVENT_PATH) as event_file:
        event_json = event_file.read()

    event    = json.loads(event_json)
    response = lambda_handler(event, None)

    print inspect_json(response)

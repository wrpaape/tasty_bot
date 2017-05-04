#!/usr/bin/env python
import os
import json

from lambda_handler import lambda_handler


EVENT_PATH = os.path.join(os.path.dirname(__file__),
                          'data', 'test_event.json')


if __name__ == '__main__':
    with open(EVENT_PATH) as event_file:
        event_json = event_file.read()

    event = json.loads(event_json)

    lambda_handler(event, None)

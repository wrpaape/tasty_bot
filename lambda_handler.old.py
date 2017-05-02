import random
import json
import traceback



# Global Variables
# ------------------------------------------------------------------------------
APPLICATION_ID         = 'dummy_application_id' # populate before publishing
APPLICATION_VERSION    = '1.0'
FLIP_COIN_INSTRUCTIONS = 'You can ask me to flip a coin for you by saying, ' \
                         'Tasty Bot, flip a coin.'



# Utility Functions
# ------------------------------------------------------------------------------
def build_response(card_title, speech_output, should_end_session):
    return {
        'version':           APPLICATION_VERSION,
        'sessionAttributes': {},
        'response': {
            'shouldEndSession': should_end_session,
            'outputSpeech': {
                'type': 'PlainText',
                'text': speech_output
            },
            'card': {
                'type':    'Simple',
                'title':   'SessionSpeechlet - ' + card_title,
                'content': 'SessionSpeechlet - ' + speech_output,
            },
            'reprompt': {
                'outputSpeech': {
                    'type': 'PlainText',
                    'text': 'Does not compute. ' + FLIP_COIN_INSTRUCTIONS,
                },
            },
        },
    }


def inspect_json(json_dict):
    return json.dumps(json_dict, indent=4, sort_keys=True)


def log_event(event_handler):
    def _log_event(event, *args):
        try:
            response = event_handler(*args)
            result   = inspect_json(response)
        except:
            response = None
            result   = traceback.format_exc()

        border    = '=' * 80
        log_entry = ''.join(('\n\n', border,
                             '\n\nhandler: ', event_handler.func_name,
                             '\n\nevent:   ', inspect_json(event),
                             '\n\nresult:  ', result,
                             '\n\n', border))
        print log_entry

        return response

    return _log_event



# Intent Handlers
# ------------------------------------------------------------------------------
def handle_help_intent():
    return build_response('Help',
                          'Hello, this is Tasty Bot. ' + FLIP_COIN_INSTRUCTIONS,
                          False)


def handle_flip_coin_intent():
    outcome = random.choice(('heads', 'tails'))

    return build_response('FlipCoin',
                          'Your coin flip outcome was ' + outcome + '.',
                          True)


INTENT_DISPATCH = {
    'FlipCoinIntent':    handle_flip_coin_intent,
    'AMAZON.HelpIntent': handle_help_intent,
}



# Event Handlers
# ------------------------------------------------------------------------------
@log_event
def handle_new_session():
    return None


@log_event
def handle_launch_request(_request):
    return handle_help_intent()


@log_event
def handle_intent_request(request):
    intent_name = request['intent']['name']

    if intent_name not in INTENT_DISPATCH:
        raise NotImplementedError(intent_name)

    intent_handler = INTENT_DISPATCH[intent_name]
    return intent_handler()


@log_event
def handle_session_ended_request(_request):
    return None


REQUEST_DISPATCH = {
    'LaunchRequest':       handle_launch_request,
    'IntentRequest':       handle_intent_request,
    'SessionEndedRequest': handle_session_ended_request,
}



# Entry Point
# ------------------------------------------------------------------------------
def lambda_handler(event, _context):
    session = event['session']

    if session['application']['applicationId'] != APPLICATION_ID:
        raise ValueError('Invalid Application ID')

    if session['new']:
        return handle_new_session(event)

    request      = event['request']
    request_type = request['type']

    if request_type not in REQUEST_DISPATCH:
        raise NotImplementedError(request_type)

    handle_request = REQUEST_DISPATCH[request_type]
    return handle_request(event, request)

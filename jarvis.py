"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function


def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    if (event['session']['application']['applicationId'] != "amzn1.echo-sdk-ams.app.10971b77-8be1-4b2e-96af-4d62794c32d9"):
        raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "resistor":
        return resistor_decode(intent, session)
    elif intent_name == "AMAZON.StartOverIntent":
        return start_over()
    elif intent_name == "AMAZON.CancelIntent":
        return get_stop_response()
    elif intent_name == "AMAZON.StopIntent":
        return get_stop_response()
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here

# --------------- Functions that control the skill's behavior ------------------


def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "I'm Jarvis, your workshop assistant. " \
                    "I'm learning to answer electrical engineering questions, " \
                    "Ask me, color code red black brown."
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Ask me about resistor color codes or calculations. " \
                    "Request new features at jarvis dash skill dot com"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_stop_response():
    session_attributes = {}
    card_title = "Bye"
    speech_output = "Glad I could help."
    reprompt_text = "Bye"
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, True))

RESISTOR_VALUES = [
    ('black', 0, 1),
    ('brown', 1, 10),
    ('red', 2, 100),
    ('orange', 3, 1000),
    ('yellow', 4, 10000),
    ('green', 5,  100000),
    ('blue', 6,   1000000),
    ('violet', 7, 10000000),
    ('gray', 8,   100000000),
    ('white', 9,  1000000000),
    ('gold', -1, .1),
    ('silver', -1, .01)
]


def simplify_num(val):
    return val if val != int(val) else int(val)


def resistor_decode(intent, session):
    """ Sets the color in the session and prepares the speech to reply to the
    user.
    """

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    color_one = intent['slots']['one']['value']
    color_two = intent['slots']['two']['value']
    color_three = intent['slots']['three']['value']
    # color_four = intent['slots']['four']['value']
    value = (([val[1] for val in RESISTOR_VALUES if val[0] == color_one][0] * 10) + 
        [val[1] for val in RESISTOR_VALUES if val[0] == color_two][0]) * \
        [val[2] for val in RESISTOR_VALUES if val[0] == color_three][0]
    unit = ''
    session_attributes = {'resistor': value}
    if value > 1000000:
        value = value / 1000000.0
        unit = ' meg'
    if value > 1000:
        value = value / 1000.0
        unit = ' k'
    speech_output = 'resistor is ' + str(simplify_num(value)) + unit + ' ohms'
    reprompt_text = "anything else?"
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def start_over():
    session_attributes = {}
    return build_response(session_attributes, build_speechlet_response(
        "Reset", "OK", "Reset", False))

# --------------- Helpers that build all of the responses ----------------------


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': 'Jarvis - ' + title,
            'content': 'Jarvis - ' + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }

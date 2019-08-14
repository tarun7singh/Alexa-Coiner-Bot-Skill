from __future__ import print_function
import requests, random, boto3
currency_names = ["Bitcoin", "Ethereum", "Ripple", "Bitcoin Cash", "Litecoin", "Cardano", "Neo", "Stellar", "Eos", "Iota", "Dash", "Monero", "Nem", "Ethereum Classic", "Lisk", "Tron", "Vechain", "Qtum", "Bitcoin Gold", "Tether"]
default_fiat = "USD"
# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "" + title,
            'content': "" + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }

def build_directive_response(title, output, reprompt_text, intent, directive_type, slot, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "" + title,
            'content': "" + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session,
        'directives': [
            {
                "type" : "Dialog.ElicitSlot",
                "slotToElicit" : slot,
                "updatedIntent" : intent
            }
        ]
    }

def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }

# --------------- Functions that control that help in skill's tasks ------------------

def get_user_prefs(UserId):
    client = boto3.client('dynamodb')
    response = client.get_item(
        TableName='UserPref',
        Key={
            'UserId': {
                'S': UserId
                }
            })
    if 'Item' in response:
        return {'fiat_currency' : response['Item']['fiat_currency']['S']}
    else:
        return {}

def set_user_prefs(UserId, user_prefs, temp_fiat):
    client = boto3.client('dynamodb')
    response = client.put_item(
        TableName='UserPref',
        Item={  "UserId": {
                "S": UserId
                },
                "fiat_currency": {
                    "S": temp_fiat
                }
            })
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return True
    else:
        return False

def fetchPrice(coin, fiat_currency):
    URL = "https://api.coinmarketcap.com/v1/ticker/" + coin +"/" + "?convert=" + fiat_currency
    r = requests.get(URL)
    if r.status_code == 200:
        r = r.json()
        price = float(r[0]['price_' + fiat_currency.lower()])
        if price < 1 and price > 0:
            return round(price, 6)
        else:
            return round(price, 3)
    else:
        return False

def locale_based_currency(user_locale):
    locale_fiat = {'en-GB' : 'GBP', 'en-US' : 'USD', 'en-CA' : 'CAD', 'en-AU' : 'AUD', 'en-IN': 'INR'}
    return locale_fiat[user_locale]

# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the Coiner bot Skill. " \
                    "You can get price of more than 100 cryptocurrencies by saying, " \
                    "Get me the price of " + random.choice(currency_names) + " . " \
                    "You can also set your default fiat currency by saying, " \
                    "Set my default fiat currency" + random.choice(['US Dollars', 'Indian Rupees', 'yen', 'pounds', 'euros']) + " ."
    
    reprompt_text = "You can ask me the price of a cryptocurrency by saying, " \
                    "Give me current price of " + random.choice(currency_names) + "."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def handle_session_end_request():
    card_title = "Good Bye"
    speech_output = "Thank you for using coiner bot skill. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

def price(intent, session, locale):
    fiat_currency_dict = {"USD": "US Dollars","AUD": "Australian Dollars","CAD": "Canadian Dollars","CHF": "Swiss francs","EUR": "Euros","GBP": "British Pounds","INR": "Rupees","JPY": "Yens","NZD": "New Zealand dollars"}

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    user_prefs = get_user_prefs(session['user']['userId'])
    
    if 'fiat_currency' in user_prefs:
        current_fiat = user_prefs['fiat_currency']
    else:
        current_fiat = locale_based_currency(locale)

    if 'coin' in intent['slots']:
        if 'resolutions' in intent['slots']['coin']:
            resolution = intent['slots']['coin']['resolutions']['resolutionsPerAuthority'][0]
            if resolution['status']['code'] == 'ER_SUCCESS_MATCH':
                coin = resolution['values'][0]['value']['name']
                price = fetchPrice(coin, current_fiat)
                if price:
                    speech_output = "The current price of " + coin + " is about "+ str(price) + ' ' + fiat_currency_dict[current_fiat]
                    reprompt_text = None
                    should_end_session = True
                else:
                    speech_output = "Error occured in getting price of " + coin
                    reprompt_text = None
            elif resolution['status']['code'] == 'ER_SUCCESS_NO_MATCH':
                coin = intent['slots']['coin']['value']
                speech_output = "Sorry, I don't know price of  " + coin + " yet. We are adding more coins soon." 
                reprompt_text = None
        else:
            speech_output = "Which cryptocurrency do you want price of?"
            reprompt_text = "Tell me the name of cryptocurrency you want price of?"
            return build_response(session_attributes, build_directive_response(card_title, speech_output, reprompt_text, intent, "Dialog.ElicitSlot", "coin", should_end_session))
            
    else:
        reprompt_text = "I'm not sure which cryptocurrency do you want price of, " \
                        "Get me the price of " + random.choice(currency_names) + "."
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def set_default(intent, session):
    
    card_title = intent['name']
    session_attributes = {}
    should_end_session = False
    
    user_prefs = get_user_prefs(session['user']['userId'])
    
    if 'currency' in intent['slots']:
        if 'resolutions' in intent['slots']['currency']:
            resolution = intent['slots']['currency']['resolutions']['resolutionsPerAuthority'][0]
            if resolution['status']['code'] == 'ER_SUCCESS_MATCH':
                temp_fiat = resolution['values'][0]['value']['name']
                set_user_prefs(session['user']['userId'], user_prefs, temp_fiat)
                speech_output = "I have set your default fiat currency to " + temp_fiat + "." 
                reprompt_text = None
                should_end_session = True
            elif resolution['status']['code'] == 'ER_SUCCESS_NO_MATCH':
                temp_fiat = intent['slots']['currency']['value']
                speech_output = "Sorry, I can't set default fiat currency to  " + temp_fiat + "." \
                                "For list of fiat currencies i support visit skill details." 
                reprompt_text = None
                should_end_session = False
        else:
            speech_output = "Which fiat currency do you want me to set as default?"
            reprompt_text = "Tell me the name of fiat currency you want to set as default?"
            should_end_session = False
            return build_response(session_attributes, build_directive_response(card_title, speech_output, reprompt_text, intent, "Dialog.ElicitSlot", "currency", should_end_session))
            
    else:
        speech_output = "I'm not sure which fiat currency you want to set as default, " \
                        "You can say " \
                        "Set my default fiat currency" + random.choice(["US Dollars","yen","Rupees", "Euros"]) + " ."
        reprompt_text = None
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
    
# --------------- Events ------------------

def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()

def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.
    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']
    locale = intent_request['locale']
    # Dispatch to your skill's intent handlers
    if intent_name == "GetPriceIntent":
        return price(intent, session, locale)
    elif intent_name == "SetDefault":
        return set_default(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")

# --------------- Main handler ------------------

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
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    # raise ValueError("Invalid Application ID")


    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
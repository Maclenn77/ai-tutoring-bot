import json
from lib.menu import Menu

def process_event(event):
    message = json.loads(event['body'])
    chat_info = message.get('message', message.get('my_chat_member')).get('chat')
    message_info = {
        'message_id': message.get('message').get('message_id'),
        'text': message.get('message').get('text')
    }

    text = message_info['text']
    options = Menu()

    if text is None:
        options.no_text(chat_info['id'])
        return
    elif text == "/start":
        options.start(chat_info)
        return
    elif text == "/help":
        options.help(chat_info['id'])
        return
    elif text == "/about":
        options.about(chat_info['id'])
        return
    elif text.split(' ')[0] == "/subject":
        options.subject(chat_info['id'], text)
        return
    else:
        options.interaction(chat_info['id'], text)
    return

# Enrich logging with contextual information from Lambda

def lambda_handler(event, context):
    process_event(event)
    return {
        "statusCode": 200
    }

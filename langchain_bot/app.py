import os
import json
from lib import dynamodb as dyn
from lib import menu

config = {
    "TELEGRAM_TOKEN": os.environ['TELEGRAM_TOKEN'],
    "OPENAI_API_KEY": os.environ['OPENAI_API_KEY'],
}

# Write Telegram Bot Token
def process_event(event):
    message = json.loads(event['body'])
    db_table = dyn.DynamoDB('AITutoringTable')
    chat_info = message.get('message', message.get('my_chat_member')).get('chat')
    message_info = {
        'message_id': message.get('message').get('message_id'),
        'text': message.get('message').get('text')
    }

    text = message_info['text']
    options = menu.Menu(config, db_table)

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

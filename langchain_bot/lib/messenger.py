import requests

# Send Messages to APIs
class Messenger:
    """Send messages to Telegram and OpenAI API"""

    def __init__(self, config):
        telegram_url = "https://api.telegram.org/bot{}/".format(config['TELEGRAM_TOKEN'])
        self.tgr_url = telegram_url + "sendMessage"

    def send_to_telegram(self, message, chat_id):
        params = {"chat_id": chat_id, "text": message}
        return requests.post(self.tgr_url, data=params)


    
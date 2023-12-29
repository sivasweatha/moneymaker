import slack
import ssl

class SendToSlack:
    def __init__(self, token: str):
        self.client = slack.WebClient(token=token, ssl=ssl.SSLContext())

    def send_message(self, message, channel="#auto-trading"):
        self.client.chat_postMessage(channel=channel, text=message)

    def slack_print(self, message, channel = None):
        print(message)
        self.send_message(message, channel)
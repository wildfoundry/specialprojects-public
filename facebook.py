import sys
import json
import requests
from rpi_leds import LED_COLOR as rpi_led_color

SUBSCRIPTION_TOKEN = "tok_dp_fb_term"

MAX_MSG_LEN = 300

GRAPH_API = "https://graph.facebook.com/v2.6/me/messages"

ACCESS_TOKEN = "EAAI3ZCiMmzZAIBAJ4LrseOAolbNbj4pDQhWN0vnDyUkqrL6XQ1u9mdJlawLZA8uoBkJwcYRxDO2ggZARZBokGkWkrrzeVO8BRM5aWegVWnLbXHqVQtHzLuulu5wJxQZCGfKCdfkFiK220ZAr4Twc4qqrwo7dZAIm9lhO4XIPXrkxSICNZAlVvQgm0"


class Facebook_messages():

    def __init__(self):
        pass

    def _split_msg(self, text):
        """
        Facebook doesn't allows messages longer than MAX_MSG_LEN in chat windows.
        This function cuts messages exceeding MAX_MSG_LEN and returns
        a list of appropriately trimmed messages.
        """
        text = [text[i:i+MAX_MSG_LEN]
                  for i in range(0, len(text), MAX_MSG_LEN)]
        return text

    def simple_msg(self, recipient_id, message_text):
        """
        This function is used to send chat messages that don't exceed MAX_MSG_LEN.
        """
        params = {"access_token": ACCESS_TOKEN}
        headers = {"Content-Type": "application/json"}
        data = json.dumps({
            "recipient": {
                "id": recipient_id
            },
            "message": {
                "text": message_text
            }
            })

        print("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

        r = requests.post(GRAPH_API, params=params, headers=headers, data=data)
        if r.status_code != 200:
            print(r.status_code)
            print(r.text)

    def long_msg(self, recipient_id, message_text):
        """
        This function is used to send chat messages which length is not known
        at the time of writing.
        """
        if len(message_text) > MAX_MSG_LEN:
            msg_list = self._split_msg(message_text)
            for i in msg_list:
                self.simple_msg(recipient_id, i)
        else:
            self.simple_msg(recipient_id, message_text)

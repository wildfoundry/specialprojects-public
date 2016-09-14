from flask import Flask, request
from terminal import Terminal
import facebook
import rpi_leds

# Flask APP
HOST = "0.0.0.0"
PORT = 80

# Dependencies
term = Terminal()
fb = facebook.Facebook_messages()
app = Flask(__name__)


@app.route('/', methods=['GET'])
def subscription():
    """
    This function handles web hook subscription request. The hub.challenge is sent
    back to facebook upon succesfull verification.
    """
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == facebook.SUBSCRIPTION_TOKEN:
            return "Verification token mismatch", 403

        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():
    """
    This it the main function where facebook chat messages are sent and received.
    """
    data = request.get_json()

    if data["object"] == "page":

        for entry in data["entry"]:
            for msg_event in entry["messaging"]:

                sender_id = msg_event["sender"]["id"]

                # Message event
                if msg_event.get("message"):
                    message_text = msg_event["message"]["text"]

                    # Help
                    if message_text == "help":
                        fb.simple_msg(sender_id, "1. To enter into terminal mode please send command \"term\"")

                    # Terminal mode
                    elif message_text == "term" and term.term_started == False:
                        term.start_terminal()
                        fb.simple_msg(sender_id, "<<< Term mode: Started >>>")
                        fb.simple_msg(sender_id, term.execute_command("pwd"))

                    elif message_text == "term" and term.term_started == True:
                        fb.simple_msg(sender_id, "<<< Term mode: Already running >>>")

                    elif message_text != "term" and term.term_started == True:
                        fb.simple_msg(sender_id, "<<< Term mode >>>")
                        fb.long_msg(sender_id, term.execute_command(message_text))

                    # Echo unrecognized commands
                    else:
                        fb.simple_msg(sender_id, "Command not found: " + message_text)

    return "ok", 200


if __name__ == '__main__':
    print(" * Starting Server")
    app.run(host=HOST, port=PORT)

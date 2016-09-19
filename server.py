from flask import Flask, request
from terminal import Terminal
import facebook
import datetime
import argparse

# Flask APP
HOST = "0.0.0.0"
PORT = 80

# Dependencies
time_now = datetime.datetime.now()
term = Terminal()
fb = facebook.Facebook_messages()
app = Flask(__name__)

arg_parser = argparse.ArgumentParser(description="Facebook Terminal Server")
arg_parser.add_argument("password", type=str, help="Password set for terminal access from facebook.")
args = arg_parser.parse_args()

# Commands
TERM = "term "
DATE = "date"
TIME = "time"
HELP = "help"

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
    This is the main function where facebook chat messages are sent and received.
    """
    data = request.get_json()

    if data["object"] == "page":

        for entry in data["entry"]:
            for msg_event in entry["messaging"]:

                sender_id = msg_event["sender"]["id"]

                # Message event
                if msg_event.get("message"):
                    try:
                        message_text = msg_event["message"]["text"]
                    except:
                        fb.simple_msg(sender_id, "Server Warning: Only messages containing text are valid.")
                        return "ok", 200

                    # Help
                    if message_text == HELP and term.term_started == False:
                        fb.simple_msg(sender_id, "1. Enter terminal mode by sending: " + TERM + "<password>"
                                               + "\nTo exit terminal mode send: exit")
                        fb.simple_msg(sender_id, "2. See current time on a Raspberry Pi by sending: " + TIME)
                        fb.simple_msg(sender_id, "3. See current date on a Raspberry Pi by sending: " + DATE)

                    # Normal mode commands
                    elif message_text == DATE and term.term_started == False:
                        fb.simple_msg(sender_id, time_now.strftime("%d-%m-%Y"))

                    elif message_text == TIME and term.term_started == False:
                        fb.simple_msg(sender_id, time_now.strftime("%H:%M"))

                    # Terminal mode
                    elif message_text == TERM + args.password and term.term_started == False:
                        term.start_terminal()
                        fb.simple_msg(sender_id, "<<< Term mode: Started >>>")
                        fb.simple_msg(sender_id, term.execute_command("pwd"))

                    elif message_text == TERM + args.password and term.term_started == True:
                        fb.simple_msg(sender_id, "<<< Term mode: Already running >>>")

                    elif message_text != TERM + args.password and term.term_started == True:
                        fb.simple_msg(sender_id, "<<< Term mode >>>")
                        fb.long_msg(sender_id, term.execute_command(message_text))

                    # Echo unrecognized commands
                    else:
                        fb.simple_msg(sender_id, "Command not found: " + message_text)
                        fb.simple_msg(sender_id, "To view command help page send: " + HELP)

    return "ok", 200


if __name__ == '__main__':
    print(" * Starting Server")
    print(" * Facebook Terminal password: " + args.password)
    app.run(host=HOST, port=PORT)

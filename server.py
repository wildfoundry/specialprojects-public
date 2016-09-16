from flask import Flask, request
from terminal import Terminal
import facebook
import rpi_leds
import datetime

# Flask APP
HOST = "0.0.0.0"
PORT = 80

# Dependencies
time_now = datetime.datetime.now()
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
                    if message_text == "help" and term.term_started == False:
                        fb.simple_msg(sender_id, "1. To enter into terminal mode please send command \"term\" (To exit use \"exit\" when in term mode)")
                        fb.simple_msg(sender_id, "2. To see current time on a Raspberry Pi please enter command \"time\"")
                        fb.simple_msg(sender_id, "3. To see current date on a Raspberry Pi please enter command \"date\"")

                    # Normal mode commands
                    elif message_text == "date" and term.term_started == False:
                        fb.simple_msg(sender_id, time_now.strftime("%d-%m-%Y"))
                        pass

                    elif message_text == "time" and term.term_started == False:
                        fb.simple_msg(sender_id, time_now.strftime("%H:%M"))
                        pass

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

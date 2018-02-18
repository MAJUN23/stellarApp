#Python libraries that we need to import for our bot
import random
from flask import Flask, request
from pymessenger.bot import Bot

app = Flask(__name__)
ACCESS_TOKEN = 'EAAIfANooh8QBAJeDEnWvbzEF2SOpmtL7dWCWGiZCXFZCdeaDP04FtQv4ZBKltZCKkm4aNPA7rdUUvvFMRB6o7YHFLwCRB92iNLHZBFpFQSX2gXkSBKZCEW1yhgbA5IoZAmwF1Yj2j6adYimhmVZC75EOBRZBf03Lq8PZCvZBRJJmZCuaf9nMjaP6N86P'
VERIFY_TOKEN = 'VERIFY_TOKEN'
bot = Bot(ACCESS_TOKEN)

#We will receive messages that Facebook sends our bot at this endpoint 
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook.""" 
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        # get whatever message a user sent the bot
       output = request.get_json()
       for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:
            if message.get('message'):
                #Facebook Messenger ID for user so we know where to send response back to
                recipient_id = message['sender']['id']
                print(message)
                if message['message'].get('text'):
                    sender_info = parse_fake_message(message['message'].get('text'))
                    response_sent_text = fake_message(sender_info[0], sender_info[1])
                    send_message(recipient_id, response_sent_text)
                #if user sends us a GIF, photo,video, or any other non-text item
                if message['message'].get('attachments'):
                    response_sent_nontext = get_message()
                    send_message(recipient_id, response_sent_nontext)
    return "Message Processed"


def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error 
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

def fake_message(amount, name):
    return "Success! You just sent {} XLM to {}".format(amount, name)

def parse_fake_message(message):
    tokens = message.split()

    if (len(tokens) < 3):
        return 
    name = tokens[1]
    amount = tokens[2]
    return (name, amount,)


#chooses a random message to send to the user
def get_message():
    sample_responses = ["Will we finish?", "Stellar is cool", "XML!", "Account Balance: 0 XLM :)"]
    # return selected item to the user
    return random.choice(sample_responses)

#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    print(type(recipient_id))
    bot.send_text_message(recipient_id, response)
    return "success"

if __name__ == "__main__":
    app.run()

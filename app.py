from flask import Flask, request
import json
import requests
import telegram
from rslashbot.credentials import botToken, botUsername, herokuURL

# Bot API Token
global bot
global TOKEN
TOKEN = botToken
bot = telegram.Bot(token=TOKEN)

# Init Flask App
app = Flask(__name__)

#Response Function to respond to Telegram API calls


@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
    """
    Responds to slash commands issued to bot via Telegram
    """

    # Retrieve message in JSON and transform it to Telegram object
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id
    msg_id = update.message.message_id

    # UTF-8 formatting
    text = update.message.text.encode('utf-8').decode()
    # for debugging
    print("Got text message: ", text)

    ### Slash Command
    # Welcome message / Start Message
    if text == "/start":
        bot_welcome = """
        Hello. This is rSlashBot. Give me a subreddit from which you wish to receive updates from.
        """
        bot.sendMessage(chat_id=chat_id, text=bot_welcome,
                        reply_to_message_id=msg_id)

    else:
        try:
            # Clear non-alphabets from message
            text = re.sub(r"\W", "_", text)
            # create the api link for the avatar based on http://avatars.adorable.io/
            url = "https://www.reddit.com/r/{}".format(text.strip())
           # reply with a photo to the name the user sent,
           # note that you can send photos by url and telegram will fetch it for you
            r = requests.get(
                url, headers={'User-agent': 'rSlashBot'}, allow_redirects=True)
            with open('reddit.json', 'wb') as f:
                f.write(r.content)
            with open('reddit.json', 'r') as f:
                l = json.load(f)
            title = l["data"]["children"][0]["data"]["title"]
            content = l["data"]["children"][0]["data"]["selftext"]
            title_text = "**"+title+"**"

            bot.sendMessage(chat_id=chat_id, text=title_text,
                            reply_to_message_id=msg_id)
            bot.sendMessage(chat_id=chat_id, text=content,
                            reply_to_message_id=msg_id)

        except Exception:
            # if things went wrong
            bot.sendMessage(
                chat_id=chat_id, text="I am sorry. There was an error fetching from that subreddit.", reply_to_message_id=msg_id)

    return 'ok'


@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
    s = bot.set_webhook('{URL}{HOOK}'.format(URL=herokuURL, HOOK=TOKEN))

    # debugging prints
    if s:
        return "Webhook setup OK"
    else:
        return "Webhook setup failed"


@app.route('/')
def index():
    return '.'


if __name__ == '__main__':
    app.run(threaded=True)

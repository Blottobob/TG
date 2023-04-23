import telegram
import requests

# Replace the following with your own bot token
bot = telegram.Bot(token='6168047438:AAFxf5Kx99LLG6eGMobs-DzoG7fXuDDq_8U')

# Replace this with your own approval code
approval_code = '@Peaky-xD'

def send_sms(number, text):
    url = 'http://mshastra.com/sendurlcomma.aspx'
    params = {
        'user': '20102108',
        'pwd': 'Sel@123',
        'senderid': 'SELFTECH',
        'CountryCode': '880',
        'mobileno': number,
        'msgtext': text
    }
    response = requests.get(url, params=params)
    return response.text

def handle_message(update, context):
    text = update.message.text
    chat_id = update.message.chat_id
    
    if text.startswith('/start'):
        reply = f'Nigqa you are not premium user. 😑🔪 \nTo get access contact @toxic_mahir\n/approval [code]'
    elif text.startswith('/approval'):
        code = text.split()[1]
        if code == approval_code:
            context.user_data['approved'] = True
            reply = 'Your approval code has been accepted. Please enter the phone number and message you want to send in the following format:\n\n/number 017xxxxxxx\n/message Hello World!'
        else:
            reply = 'Sorry, your approval code was not recognized.'
    elif 'approved' in context.user_data and context.user_data['approved']:
        if text.startswith('/number'):
            number = text.split()[1]
            context.user_data['number'] = number
            reply = f'Phone number set to {number}. Please enter your message now.'
        elif text.startswith('/message'):
            if 'number' in context.user_data:
                number = context.user_data['number']
                message = ' '.join(text.split()[1:])
                send_sms(number, message)
                reply = f'SMS sent to {number}: {message}'
            else:
                reply = 'Please enter a phone number first.'
        else:
            reply = 'Sorry, I did not understand that command.'
    else:
        reply = 'Please enter your approval code first using the /approval command.'
    
    context.bot.send_message(chat_id=chat_id, text=reply)

if __name__ == '__main__':
    from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
    
    updater = Updater(token='6168047438:AAFxf5Kx99LLG6eGMobs-DzoG7fXuDDq_8U', use_context=True)
    dispatcher = updater.dispatcher
    
    # Add handlers for different types of Telegram messages
    start_handler = CommandHandler('start', handle_message)
    approval_handler = CommandHandler('approval', handle_message)
    number_handler = CommandHandler('number', handle_message)
    message_handler = CommandHandler('message', handle_message)
    unknown_handler = MessageHandler(Filters.command, handle_message)
    
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(approval_handler)
    dispatcher.add_handler(number_handler)
    dispatcher.add_handler(message_handler)
    dispatcher.add_handler(unknown_handler)
    
    updater.start_polling()

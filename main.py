import os

import requests

from telegram import Bot, InputFile

from telegram.ext import CommandHandler, Updater, CallbackContext

# Telegram bot token

TOKEN = '6242918828:AAHH0M0GZC4rjF57bZIvbFMMaOCSSs0ZsHw'

# Initialize the bot

bot = Bot(TOKEN)

def download_and_upload(update, context):

    # Get the direct download link from the message

    link = update.message.text.split(' ')[1]

    # Download the file

    response = requests.get(link)

    file_name = link.split('/')[-1]

    with open(file_name, 'wb') as file:

        file.write(response.content)

    # Rename the file

    new_file_name = 'new_' + file_name

    os.rename(file_name, new_file_name)

    # Get the current value of upload_as_document flag

    upload_as_document = context.user_data.get('upload_as_document', False)

    # Upload the file to Telegram

    if upload_as_document:

        with open(new_file_name, 'rb') as file:

            bot.send_document(chat_id=update.message.chat_id, document=file)

    else:

        with open(new_file_name, 'rb') as file:

            bot.send_photo(chat_id=update.message.chat_id, photo=InputFile(file))

    # Delete the temporary file

    os.remove(new_file_name)

def set_upload_as_document(update, context):

    # Get the choice from the message

    choice = update.message.text.split(' ')[1].lower()

    if choice == 'true':

        context.user_data['upload_as_document'] = True

        update.message.reply_text('Upload as document set to True')

    elif choice == 'false':

        context.user_data['upload_as_document'] = False

        update.message.reply_text('Upload as document set to False')

    else:

        update.message.reply_text('Invalid choice. Please use either True or False.')

def help_command(update, context):

    help_text = '''

    This is a file download and upload bot.

    Available commands:

    - /download <direct_link>: Downloads a file from the provided direct link and uploads it to Telegram.

    - /set_upload_as_document <true/false>: Sets whether to upload as a document or media.

    Note: By default, files are uploaded as media.

    '''

    update.message.reply_text(help_text)

# Handler for the '/download' command

download_handler = CommandHandler('download', download_and_upload)

# Handler for the '/set_upload_as_document' command

set_upload_handler = CommandHandler('set_upload_as_document', set_upload_as_document)

# Handler for the '/help' command

help_handler = CommandHandler('help', help_command)

updater = Updater(TOKEN, use_context=True)

dispatcher = updater.dispatcher

dispatcher.add_handler(download_handler)

dispatcher.add_handler(set_upload_handler)

dispatcher.add_handler(help_handler)

updater.start_polling()


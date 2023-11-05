#!/usr/bin/env python
import logging
from dotenv import dotenv_values

from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from telegram import Update

config = {
    **dotenv_values(".env")
}

# pylint: disable=unused-argument

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# Define a `/start` command handler.
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start command"""
    await update.message.reply_text(
        f"I am {config['BOT_USERNAME']}."
    )

# help command handler


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sample help command"""
    await update.message.reply_text(
        f"I am {config['BOT_USERNAME']}. Please type something so I can respond!"
    )


# Responses
def handle_response(text: str) -> str:
    """Sample response handler. Currently a if / else"""
    processed: str = text.lower()
    if 'hello' in processed:
        return 'hey there'


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sample message handler"""
    # check if group chat / private chat
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':
        if config['BOT_USERNAME'] in text:
            new_text: str = text.replace(config['BOT_USERNAME'], '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)

    print('Bot: ', response)
    await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sample error handler"""
    print(f'Update {update} caused error {context.error}')


def main() -> None:
    """Start the bot."""
    # create application with telegram bot token
    application = Application.builder().token(config["TOKEN"]).build()

    # commands
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))

    # messages
    application.add_handler(MessageHandler(filters.TEXT, handle_message))

    # errors
    application.add_error_handler(error)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()

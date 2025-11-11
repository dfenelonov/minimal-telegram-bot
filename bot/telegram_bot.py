from __future__ import annotations

import asyncio
import logging
import os
import io

from uuid import uuid4
from telegram import BotCommandScopeAllGroupChats, Update, constants
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultArticle
from telegram import InputTextMessageContent, BotCommand
from telegram.error import RetryAfter, TimedOut, BadRequest
from telegram.ext import ApplicationBuilder, CommandHandler, Application, ContextTypes

from utils import error_handler


class ChatGPTTelegramBot:
    """
    Class representing a ChatGPT Telegram Bot.
    """

    def __init__(self, config: dict):
        """
        Initializes the bot with the given configuration and GPT bot object.
        :param config: A dictionary containing the bot configuration
        :param openai: OpenAIHelper object
        """
        self.config = config
        self.commands = [
            BotCommand(command='help', description='help_description'),
        ]
        # If imaging is enabled, add the "image" command to the list

        self.usage = {}
        self.last_message = {}
        self.inline_queries_cache = {}

    async def help(self, update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Shows the help menu.
        """
        commands = self.commands
        commands_description = [f'/{command.command} - {command.description}' for command in commands]
        help_text = (
                "ОГО Я ТАКОЙ ПОЛЕЗНЫЙ"
        )
        await update.message.reply_text(help_text, disable_web_page_preview=True)


    async def post_init(self, application: Application) -> None:
        """
        Post initialization hook for the bot.
        """
        await application.bot.set_my_commands(self.commands)

    def run(self):
        """
        Runs the bot indefinitely until the user presses Ctrl+C
        """
        application = ApplicationBuilder() \
            .token(self.config['token']) \
            .post_init(self.post_init) \
            .concurrent_updates(True) \
            .build()

        application.add_handler(CommandHandler('help', self.help))
        application.add_handler(CommandHandler('start', self.help))

        application.add_error_handler(error_handler)

        application.run_polling()

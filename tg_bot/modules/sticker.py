
import html
from typing import Optional, List
import random
from telegram import Message, Chat, Update, Bot, User
from telegram import ParseMode, InlineKeyboardMarkup
from telegram.error import BadRequest
from telegram.ext import MessageHandler, Filters, CommandHandler, run_async
from telegram.utils.helpers import mention_markdown, mention_html, escape_markdown
import tg_bot.modules.sql.welcome_sql as sql
from tg_bot import dispatcher, OWNER_ID, LOGGER
from tg_bot.modules.helper_funcs.chat_status import user_admin, can_delete
from tg_bot.modules.helper_funcs.misc import build_keyboard, revert_buttons
from tg_bot.modules.helper_funcs.msg_types import get_welcome_type
from tg_bot.modules.helper_funcs.string_handling import markdown_parser, \
    escape_invalid_curly_brackets


def send(update, message, keyboard, backup_message):
    try:
        msg = update.effective_message.reply_text(message, parse_mode=ParseMode.MARKDOWN, reply_markup=keyboard)
    except IndexError:
        msg = update.effective_message.reply_text(markdown_parser(backup_message +
                                                                  "\nNote: the current message was "
                                                                  "invalid due to markdown issues. Could be "
                                                                  "due to the user's name."),
                                                  parse_mode=ParseMode.MARKDOWN)
    except KeyError:
        msg = update.effective_message.reply_text(markdown_parser(backup_message +
                                                                  "\nNote: the current message is "
                                                                  "invalid due to an issue with some misplaced "
                                                                  "curly brackets. Please update"),
                                                  parse_mode=ParseMode.MARKDOWN)
    except BadRequest as excp:
        if excp.message == "Button_url_invalid":
            msg = update.effective_message.reply_text(markdown_parser(backup_message +
                                                                      "\nNote: the current message has an invalid url "
                                                                      "in one of its buttons. Please update."),
                                                      parse_mode=ParseMode.MARKDOWN)
        elif excp.message == "Unsupported url protocol":
            msg = update.effective_message.reply_text(markdown_parser(backup_message +
                                                                      "\nNote: the current message has buttons which "
                                                                      "use url protocols that are unsupported by "
                                                                      "telegram. Please update."),
                                                      parse_mode=ParseMode.MARKDOWN)
        elif excp.message == "Wrong url host":
            msg = update.effective_message.reply_text(markdown_parser(backup_message +
                                                                      "\nNote: the current message has some bad urls. "
                                                                      "Please update."),
                                                      parse_mode=ParseMode.MARKDOWN)
            LOGGER.warning(message)
            LOGGER.warning(keyboard)
            LOGGER.exception("Could not parse! got invalid url host errors")
        else:
            msg = update.effective_message.reply_text(markdown_parser(backup_message +
                                                                      "\nNote: An error occured when sending the "
                                                                      "custom message. Please update."),
                                                      parse_mode=ParseMode.MARKDOWN)
            LOGGER.exception()

    return msg

@run_async
def new_member(bot: Bot, update: Update):
    chat = update.effective_chat  # type: Optional[Chat]
    join = update.effective_message.new_chat_members
    count = chat.get_members_count()
    if count is 3:
                update.effective_message.reply_text("Hello boy , You are first")
    elif count is 25:
                update.effective_message.reply_sticker("CAACAgEAAxkBAAKp0GCriGh4oGz56qW1wdMHUJULU-wxAAJ1AgACb8FkFDCUuHcEvpgrHwQ")
    elif count is 50:
                update.effective_message.reply_sticker("CAACAgEAAxkBAAKp02CriHTL6W6VKEDkZ7SpDuBJ-hv\_AAJ2AgACb8FkFMQhQH7icivgHwQ")               
    elif count is 75:
                update.effective_message.reply_sticker("CAACAgEAAxkBAAKp2WCrjLF-chH9sdbwfZKRweC9wDpdAAJ3AgACb8FkFNnvojLmMWChHwQ")
    elif count is 100:
                update.effective_message.reply_sticker("CAACAgEAAxkBAAKp2mCrjLK9bjhBHxRKvY6mzC29zdX-AAJ4AgACb8FkFCHyjB1WKhwIHwQ")               
    elif count is 150:
                update.effective_message.reply_sticker("CAACAgEAAxkBAAKp22CrjLMcLfLnSbQ3MCyJAAF3p5pMfQACeQIAAm\_BZBQtPpJQWxVDnB8E")
    elif count is 200:
                update.effective_message.reply_sticker("CAACAgEAAxkBAAKp3GCrjLMSlZIUA135iaT2Be9Zhri4AAJ6AgACb8FkFDqPwakq2etKHwQ")               
    elif count is 250:
                update.effective_message.reply_sticker("CAACAgEAAxkBAAKp6GCrjf9Ynb5ref88s\_gaH8jbUoofAAJ7AgACb8FkFCFLPuqC5veCHwQ")               
    elif count is 300:
                update.effective_message.reply_sticker("CAACAgEAAxkBAAKp62Crjhl9OLuO0AQXOCD9KjI-jHKNAAJ8AgACb8FkFCmoLzif0k1eHwQ")               
    elif count is 350:
                update.effective_message.reply_sticker("CAACAgEAAxkBAAKp7mCrjjfNsHWivLln\_yOc\_P8gcYT-AAJ9AgACb8FkFOItmI8tdunbHwQ")               
    elif count is 400:
                update.effective_message.reply_sticker("CAACAgEAAxkBAAKp8WCrjlPskv0cI2bjkocefjYgtkA6AAJ-AgACb8FkFLEuZPK4e-XOHwQ")               
    elif count is 450:
                update.effective_message.reply_sticker("CAACAgEAAxkBAAKp9GCrjyZ\_UJduUnF81DakBCh1buf4AAJ\_AgACb8FkFPJ2TY44h3N6HwQ")               
    elif count is 500:
                update.effective_message.reply_sticker("CAACAgEAAxkBAAKp92Crj0AwEaGbayhTtD-fk5YYax5jAAKAAgACb8FkFDdNlq54yRL6HwQ")               
    elif count is 550:
                update.effective_message.reply_sticker("CAACAgEAAxkBAAKp-mCrj1qG-X0B5fH8p2pkCgAB4jyKwgACgQIAAm\_BZBSPptVG0Fq4JB8E")               
    elif count is 600:
                update.effective_message.reply_sticker("CAACAgEAAxkBAAKp\_WCrj3PbLep6QljDXk5zvQ2DtzquAAKCAgACb8FkFM9xskyitVWxHwQ")               
    elif count is 650:
                update.effective_message.reply_sticker("CAACAgEAAxkBAAKqAAFgq4-U-ZYwN9NjQ3\_pmUA2iP3BhAACgwIAAm\_BZBQvwCFfDwjlvB8E")               
    elif count is 700:
                update.effective_message.reply_sticker("CAACAgEAAxkBAAKqA2CrkCvzVcHt1iWD3mdCzqHyBbtFAAKEAgACb8FkFHeWcxlF2xjEHwQ")               
    elif count is 750:
                update.effective_message.reply_sticker("CAACAgEAAxkBAAKqBmCrkD9fNnHje\_UKcZ7\_qEg7WtLiAAKFAgACb8FkFND5m5zAauszHwQ")               
    elif count is 800:
                update.effective_message.reply_sticker("CAACAgEAAxkBAAKqCWCrkFkkx9mTOclBopAR2WXTaqlpAAKGAgACb8FkFAZBHHiJozilHwQ")               
    elif count is 850:
                update.effective_message.reply_sticker("CAACAgEAAxkBAAKqDGCrkHNLxO\_RXjVgoz4kILONpN7DAAKHAgACb8FkFFmrvvzk7QZRHwQ")               
    elif count is 900:
                update.effective_message.reply_sticker("CAACAgEAAxkBAAKqEWCrkKOuTeR4zmIRAw7lHnT5MkXKAAKIAgACb8FkFFEX5yMmL9DLHwQ")               
    elif count is 950:
                update.effective_message.reply_sticker("CAACAgEAAxkBAAKqFGCrkMDDMLWyMWzSIoagwJyYGyk0AAKJAgACb8FkFM3a7eUdwjVxHwQ")               
    elif count is 1000:
                update.effective_message.reply_sticker("CAACAgEAAxkBAAKqGWCrkOOa5UHFZXBSrWYfO7FyvOFSAAKKAgACb8FkFBAnB\_OSoszTHwQ")               
    elif count is 1500:
                update.effective_message.reply_sticker("CAACAgEAAxkBAAKqHGCrkP9q4ZMqL9Pnm23bt-rpn1wHAAKLAgACb8FkFF7f1TftpoS3HwQ")               
    elif count is 2000:
                update.effective_message.reply_sticker("CAACAgEAAxkBAAKqH2CrkS\_LgXE7bPqTyMjUA7NSzVJjAAKMAgACb8FkFBKXkZIBPS-LHwQ")               
    elif count is 2500:
                update.effective_message.reply_sticker("CAACAgEAAxkBAAKqIGCrkTDzdwHEHYkK9Sf1Iz0sGR9hAAKNAgACb8FkFH5oCr7\_PZAlHwQ")               





NEW_MEM_HANDLER = MessageHandler(Filters.status_update.new_chat_members, new_member)
dispatcher.add_handler(NEW_MEM_HANDLER)

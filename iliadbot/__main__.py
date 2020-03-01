# iliadbot - A telegram bot to check your iliad's balance and quotas
# Copyright (C) 2018  iliadbot authors: see AUTHORS file at the top-level directory of this repo
#
# iliadbot is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# iliadbot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with iliadbot.  If not, see <http://www.gnu.org/licenses/>.


import logging

from iliadbot import commands
from iliadbot import config
from iliadbot import callbackqueries
from iliadbot import messages

from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackQueryHandler
)

from telegram.error import (TelegramError, Unauthorized, BadRequest, TimedOut, ChatMigrated, NetworkError)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)


def error(update, context):
    try:
        logger.warning('Update "%s" caused error "%s"' % (update, context.error))
    except Unauthorized as e:
        # remove update.message.chat_id from conversation list
        logger.exception(f'Errore: {e}')
    except BadRequest as e:
        # handle malformed requests - read more below!
        logger.exception(f'Errore: {e}')
    except TimedOut as e:
        # handle slow connection problems
        logger.exception(f'Errore: {e}')
    except NetworkError as e:
        # handle other connection problems
        logger.exceptio(f'Errore: {e}')
    except ChatMigrated as e:
        # the chat_id of a group has changed, use e.new_chat_id instead
        logger.exception(f'Errore: {e}')
    except TelegramError as e:
        # handle all other telegram related errors
        logger.exception(f'Errore: {e}')


def main():
    print("\nrunning...")
    # define the updater
    updater = Updater(token=config.BOT_TOKEN, use_context=True)
    
    # define the dispatcher
    dp = updater.dispatcher

    # define jobs
    j = updater.job_queue

    # messages
    dp.add_handler(MessageHandler(Filters.all, messages.before_processing), -1)

    # commands
    dp.add_handler(CommandHandler(('start', 'help'), commands.help_command))
    dp.add_handler(CommandHandler('info', commands.user_info_traffic_command))

    # handle callbackqueries
    dp.add_handler(CallbackQueryHandler(callbackqueries.callback_query))

    # handle errors
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

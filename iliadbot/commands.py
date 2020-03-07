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


import html
import logging
import string

from iliadbot import api
from iliadbot import keyboards
from iliadbot import emoji
from iliadbot import utils


def iliad_message_creation(iliad_id, iliad_password, which_dict='info_sim', t_id=0):
    login = api.login(iliad_id, iliad_password, t_id)
    intro = {
        'italia': 'Le tue soglie in Italia {}'.format(emoji.italy),
        'estero': 'Le tue soglie all\'estero {}'.format(emoji.earth),
        'info_sim': 'Info sulla tua sim {}'.format(emoji.info)
    }

    msg = ""
    if login is not None:
        info = api.get_info(login, which_dict)
        msg += "<b>{}: </b>".format(intro[which_dict])
        if len(info) == 0:  # iliad retuned nothing
            msg += "\nNon c'è nulla da mostrare"
        else:
            for i in utils.adjust_parsed_info(info):
                msg += "\n{}{}: {}".format(emoji.current_choice, html.escape(i[0]), html.escape(i[1]))
        keyboard = keyboards.update_iliad_data_kb(iliad_id, iliad_password, which_dict)
    else:  # invalid credentials
        msg += "<b>ERRORE:</b> {}".format(html.escape("ID utente o password non corretti"))
        keyboard = None
    return msg, keyboard


def user_info_traffic_command(update, context):
    if len(context.args) != 2:
        msg = (
            "Per utilizzare questo comando devi aggiungere id iliad come primo argomento e "
            "password iliad come secondo argomento.\nEsempio:\n\n<code>{} mio_id_iliad "
            "mia_password_iliad</code>"
        )
        msg = msg.format(update.message.text.split(" ")[0])
        update.message.reply_html(msg)
        return

    iliad_id, iliad_password = context.args

    try:
        int(iliad_id)
    except ValueError as e:
        logging.exception(f'Questo non sembra essere un id iliad {iliad_id}: {e}')
        update.message.reply_html('Errore nel processare la richiesta, input errati')
        return

    if any(c not in string.ascii_letters + string.digits + '][!"#$%&\'()=\{\}*+,./:;' for c in iliad_password):
        logging.error('Caratteri password non validi')
        update.message.reply_html('Errore nel processare la richiesta, input errati')
        return
    
    msg, keyboard = iliad_message_creation(iliad_id, iliad_password, t_id=update.message.from_user.id)
    update.message.reply_html(msg, reply_markup=keyboard)


def help_command(update, context):
    msg = (
        "Questo bot permette di conoscere soglie e credito della tua SIM iliad. "
        "Il bot *non è ufficiale* e *non conserva o salva le tue credenziali di accesso*, tuttavia queste potrebbero rimanere sui server di Telegram. Utilizza il bot consapevolmente!\n"
        "Il [codice sorgente](https://github.com/doublegized/iliadbot) è rilasciato sotto licenza AGPL 3.0.\n\n"
        "*COMANDI SUPPORTATI:*\n\n/info - permette di conoscere stato soglie e credito"
        "\n/help - mostra un messaggio di aiuto"
    )
    update.message.reply_markdown(msg, disable_web_page_preview=True)

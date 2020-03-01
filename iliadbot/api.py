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


import requests
import logging
from lxml import html
import re
import collections
from iliadbot import emoji

url = "https://www.iliad.it/account/"

# italia xpaths
dic_italia = collections.OrderedDict()
dic_italia["{} chiamate".format(emoji.telephone)] = "/html/body/div[1]/div[1]/div/div/div/div/div[2]/div[2]/div[3]/div[1]/div[1]/div/div[1]"
dic_italia["{} sms".format(emoji.sms)] = "/html/body/div[1]/div[1]/div/div/div/div/div[2]/div[2]/div[3]/div[1]/div[2]/div/div[1]"
dic_italia["{} internet".format(emoji.internet)] = "/html/body/div[1]/div[1]/div/div/div/div/div[2]/div[2]/div[3]/div[2]/div[1]/div/div[1]"
dic_italia["{} mms".format(emoji.mms)] = "/html/body/div[1]/div[1]/div/div/div/div/div[2]/div[2]/div[3]/div[2]/div[2]/div/div[1]"

# estero xpaths
dic_estero = collections.OrderedDict()
dic_estero["{} chiamate".format(emoji.telephone)] = "/html/body/div[1]/div[1]/div/div/div/div/div[2]/div[2]/div[4]/div[1]/div[1]/div/div[1]"
dic_estero["{} sms".format(emoji.sms)] = "/html/body/div[1]/div[1]/div/div/div/div/div[2]/div[2]/div[4]/div[1]/div[2]/div/div[1]"
dic_estero["{} internet".format(emoji.internet)] = "/html/body/div[1]/div[1]/div/div/div/div/div[2]/div[2]/div[4]/div[2]/div[1]/div/div[1]"
dic_estero["{} mms".format(emoji.mms)] = "/html/body/div[1]/div[1]/div/div/div/div/div[2]/div[2]/div[4]/div[2]/div[2]/div/div[1]"

dic_general_info = collections.OrderedDict()
dic_general_info["{} utente".format(emoji.user)] = "/html/body/div[1]/div[2]/div/nav/div/div/div[2]/div[1]"
dic_general_info["{} id utente".format(emoji.user)] = "/html/body/div[1]/div[1]/div/div/div/div/nav/div/div/div[2]/div[2]"
dic_general_info["{} numero".format(emoji.user)] = "/html/body/div[1]/div[1]/div/div/div/div/nav/div/div/div[2]/div[3]"
#dic_general_info["{} consumo totale".format(emoji.money)] = "/html/body/div[1]/div[2]/div[1]/div/div[2]/div[2]/div[6]/div[2]"   #removed from website
dic_general_info["{} credito".format(emoji.money)] = "/html/body/div[1]/div[1]/div/div/div/div/div[2]/div[2]/h2/b"
dic_general_info["{} rinnovo".format(emoji.renewal)] = "/html/body/div[1]/div[1]/div/div/div/div/div[2]/div[2]/div[2]"

credenziali_errate_path = '/html/body/div[1]/div[1]/div/div[1]/div'

def login(id_iliad, pwd, t_id):
    """
    params: id, pwd
    return: TreeObject
    """
    data = {"login-ident": id_iliad, "login-pwd":pwd}

    logging.debug(f'Effettuo login utente {t_id}')
    s = requests.Session()
    if s.get(url).status_code != 200:
        logging.error(f'Iliad server status code {r.status_code}')
        return False
    r = s.post(url, data=data)
    if r.status_code != 200:
        logging.error(f'Iliad server status code {r.status_code}')
        return False
    tree = html.fromstring(r.content)

    # Return False if wrong credentials
    logging.debug(tree.xpath(credenziali_errate_path)[0].text_content())
    if "ID utente o password non corretto." in tree.xpath(credenziali_errate_path)[0].text_content():
        logging.warning(f'Utente {t_id}: credenziali errate')
        return None

    logging.debug(f'Effettuato login per utente {t_id}')
    return tree


def get_info(tree, which_dic):
    """
    Parse iliad info from tree object of the html profile page
    
    params: TreeObject
    return: dic
    """
    logging.debug('Ricerco informazioni credito')
    info = []

    # which_dic to take
    if which_dic == 'italia':
        dic = dic_italia
    elif which_dic == 'estero':
        dic = dic_estero
    else:
        dic = dic_general_info

    for k, v in dic.items():
        res = tree.xpath(v)
        if res:
            res_child_text = res[0].text_content()
            res_child_text_no_spaces = re.sub(' +',' ', res_child_text)  # remove multiple spaces
            res_child_text_no_spaces = re.sub(' \n',' ', res_child_text_no_spaces)  # remove multiple new lines
            res_child_text_no_spaces = re.sub(' \t',' ', res_child_text_no_spaces) # remove multiple tabs
            info.append([k, res_child_text_no_spaces])
    return info

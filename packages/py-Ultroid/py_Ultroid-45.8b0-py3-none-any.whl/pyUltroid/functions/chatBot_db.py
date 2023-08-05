# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.

from .. import udB


def str_to_list(text):  # Returns List
    return text.split(" ")


def list_to_str(list):  # Returns String
    str = "".join(f"{x} " for x in list)
    return str.strip()


def are_all_nums(list):  # Takes List , Returns Boolean
    return all(item.isdigit() for item in list)


def get_all_added():  # Returns List
    cB_added = udB.get("CHATBOT_USERS")
    if cB_added is None or cB_added == "":
        return [""]
    else:
        return str_to_list(cB_added)


def chatbot_stats(id):  # Take int or str with numbers only , Returns Boolean
    if not str(id).isdigit():
        return False
    cB_added = get_all_added()
    return str(id) in cB_added


def add_chatbot(id):  # Take int or str with numbers only , Returns Boolean
    id = str(id)
    try:
        cB_added = get_all_added()
        cB_added.append(id)
        udB.set("CHATBOT_USERS", list_to_str(cB_added))
        return True
    except Exception as e:
        print(f"Ultroid LOG : // functions/chatBot_db/add_chatbot : {e}")
        return False


def rem_chatbot(id):  # Take int or str with numbers only , Returns Boolean
    id = str(id)
    try:
        cB_added = get_all_added()
        cB_added.remove(id)
        udB.set("CHATBOT_USERS", list_to_str(cB_added))
        return True
    except Exception as e:
        print(f"Ultroid LOG : // functions/chatBot_db/rem_chatbot : {e}")
        return False

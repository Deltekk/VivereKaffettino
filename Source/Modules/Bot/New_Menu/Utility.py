from hashlib import sha256
from base64 import urlsafe_b64encode


def safe_hash_name(string1: str, string2: str) -> str:
    return urlsafe_b64encode(sha256(str(string1 + "_" + string2).encode()).digest()).decode('utf-8')[:16]


ACTIONS = ["acquire_username_toregister", "acquire_age", "dataNascita", "selecting_gender", "gender",
           "selecting_auletta_registra", "auletta",
           "acquire_user_tocharge", "validate_amount_tocharge",
           "acquire_user_tomake_admin", "acquire_user_toremove_from_admin", "acquire_card_number",
           "acquire_nome_prodotto", "acquire_costo_prodotto", "confirm_new_prodotto", "auletta_4storage",
           "acquire_user_toverify", "change_card", "acquire_card_to_change", "idCard_tochange",
           "acquire_user_to_change_card", "acquire_user_toverify_keyboard", "action_to_perform",
           "username", "username_id", "idCard", "amount", "nome_prodotto", "costo_prodotto"]


ACQUIRE_USERNAME_REGISTRATION = "SRwRn962weWpk_8A"
ACQUIRE_AGE_REGISTRATION = "JIOLaLm4rDKlRBbl"
ACQUIRE_USERNAME_RECHARGE = "0M4vBDMcZnKfxed9"
ACQUIRE_AMOUNT_RECHARGE = "lcADSaGdP15eAw2i"
ACQUIRE_USERNAME_VERIFY = "_4xTaIgSUS3oZKIL"
ACQUIRE_CARD_NUMBER = "iVivD-PBK7FWrL2D"
ACQUIRE_USERNAME_ADD_ADMIN = "VbO0w6FbL_Vu1imZ"
ACQUIRE_USERNAME_REMOVE_ADMIN = "GqRI4J9kGURvhy8P"
ACQUIRE_MESSAGE_TO_SEND_ALL = "RWSxXiHZAPNZKuPI"
ACQUIRE_USERNAME_CARD_CHANGE = "IxylYTF4FvHARdOo"
ACQUIRE_CARD_NUMBER_CHANGE = "ym4rhDgd54OMJL-n"

CONVERSATION_CLASSES = ["ConversationManager", "Registration", "Recharge", "AdminMenu", "VerifyUser", "AddAdmin",
                        "RemoveAdmin", "SendMessageAll", "ChangeCard"]

GENDER_DICT = {"donna": "a", "uomo": "o", "altro": "ə"}
DB_GENDER_DICT = {"D": "a", "U": "o", "A": "ə"}

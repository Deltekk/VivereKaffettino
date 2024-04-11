from telegram import InlineKeyboardButton

# Azioni attive durante le conversazioni
ACTIONS = ["acquire_username_toregister", "acquire_age", "dataNascita", "selecting_gender", "gender",
           "selecting_auletta_registra", "auletta",
           "acquire_amount_tocharge", "validate_amount_tocharge",
           "acquire_user_tomake_admin", "acquire_user_toremove_from_admin", "acquire_card_number",
           "username", "username_id", "idCard", "chat_id", "message_id"]

GENDER_DICT = {"donna": "a", "uomo": "o", "altro": "ə"}
DB_GENDER_DICT = {"D": "a", "U": "o", "A": "ə"}

buttons_dict = {
    "back_main_menu": [[InlineKeyboardButton("❌ Annulla", callback_data='back_main_menu')]],

    "correct_acquire_username_toregister": [[InlineKeyboardButton("✔ Conferma", callback_data='age')],
                                         [InlineKeyboardButton("❌ Annulla", callback_data='back_main_menu')]],

    "wrong_acquire_username_toregister": [[InlineKeyboardButton("❌ Annulla", callback_data='back_main_menu')]],

    "correct_acquire_age": [[InlineKeyboardButton("✔ Conferma", callback_data='selecting_gender')],
                            [InlineKeyboardButton("🔙 Torna indietro", callback_data='age')]],

    "selecting_gender": [[InlineKeyboardButton("Donna", callback_data='donna')],
                           [InlineKeyboardButton("Uomo", callback_data='uomo')],
                           [InlineKeyboardButton("Altro", callback_data='altro')],
                           [InlineKeyboardButton("🔙 Torna indietro", callback_data='age')]],

    "done_selecting_gender": [[InlineKeyboardButton("✔️ Conferma", callback_data='selecting_auletta_registra')],
                           [InlineKeyboardButton("🔙 Torna indietro", callback_data='selecting_gender')]],

    "validate_amount_tocharge": [[InlineKeyboardButton("✔ Conferma", callback_data='done_ricarica')],
                    [InlineKeyboardButton("❌ Annulla", callback_data='back_main_menu')]],

    "acquire_card_number": [[InlineKeyboardButton("✔ Conferma", callback_data='acquired_card')],
                                         [InlineKeyboardButton("❌ Annulla", callback_data='back_main_menu')]],

    "admin": [[InlineKeyboardButton("Verifica Utente ☑", callback_data='acquire_user_toverify')],
                           [InlineKeyboardButton("Aggiungi Admin 🟢", callback_data='add_admin')],
                           [InlineKeyboardButton("Rimuovi Admin 🔴", callback_data='remove_admin')],
                           [InlineKeyboardButton("🔙 Ritorna al menu principale", callback_data='back_main_menu')]]
}


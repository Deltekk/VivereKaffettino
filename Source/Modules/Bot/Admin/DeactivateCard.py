from Modules.Bot.SubMenu import SubMenu
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from Modules.Shared.Query import GetMyAuletta, SetIsVerified, GetIdTelegram, GetVerifiedUsers


class DeactivateCard(SubMenu):

    def __init__(self):
        super().__init__()

        # conversation_batches = ["deactivate_card", "deactivate_user"]

        self.user_to_deactivate = ""

        self.UNVERIFIED_USERS_LIST_KEYBOARD = None

        self.INTRO_MESSAGES = {
            "deactivate_card": "Seleziona un utente dalla lista",
        }

        self.ERROR_MESSAGES = {

            "deactivate_card": "Non ci sono utenti da poter disattivare",
        }

    def set_user_to_deactivate(self, user_to_deactivate: str):
        self.user_to_deactivate = user_to_deactivate

    async def start_conversation(self, update: Update, context: ContextTypes.DEFAULT_TYPE, query=None,
                                 current_batch: str = None):
        self.query = query
        self.current_batch = current_batch
        admin_who_makes_the_query = query.from_user.id

        buttons = []
        for utente in GetVerifiedUsers(GetMyAuletta(admin_who_makes_the_query)):
            button = InlineKeyboardButton(text=utente[0], callback_data=utente[0])
            buttons.append([button])
        buttons.append([InlineKeyboardButton("🔙 Torna indietro", callback_data='manage_card')])
        self.UNVERIFIED_USERS_LIST_KEYBOARD = InlineKeyboardMarkup(buttons)

        if len(buttons) == 1:
            await query.edit_message_text(self.ERROR_MESSAGES[current_batch],
                                          reply_markup=self.UNVERIFIED_USERS_LIST_KEYBOARD)
        else:
            await query.edit_message_text(self.INTRO_MESSAGES[current_batch],
                                          reply_markup=self.UNVERIFIED_USERS_LIST_KEYBOARD)

    async def end_conversation(self, update: Update, context: ContextTypes.DEFAULT_TYPE, query=None):
        self.current_batch = ""
        SetIsVerified(GetIdTelegram(self.user_to_deactivate), False)

        keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 Ritorna al menu admin", callback_data='main_admin')]])
        await self.query.edit_message_text(
            text=f"L'utente {self.user_to_deactivate} è stato disattivato correttamente!",
            reply_markup=keyboard)

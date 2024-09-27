
from Modules.Bot.SubMenu import SubMenu
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from Modules.Shared.Query import GetNomeAuletta, GetMyAuletta, AssegnaProdotto, GetProdottiNonAssociati,\
    GetIDProdotto, GetAuletta, QuantitaECosto, GetIdGruppoTelegram, GetUsername


class NewProduct(SubMenu):

    def __init__(self):
        super().__init__()

        # conversation_batches = ["new_product", "acquire_product", "acquire_price_product", "acquire_price",
        # "product_added"]

        self.UNREGISTERED_PRODUCTS = None

        self.product_params = {

            "auletta": "",

            "acquire_product": "",

            "acquire_price": 0.
        }

        self.INTRO_MESSAGES = {

            "custom_new_product_storage": "Dimmi pure il prodotto da aggiungere",

            "acquire_product": "Sicuro di voler confermare",

            "acquire_price_product": "Ora dimmi quanto costa per favore",

            "acquire_price": "Sicuro di voler confermare"
        }

        self.KEYBOARDS = {

            "select_new_product": InlineKeyboardMarkup(
                [[InlineKeyboardButton("🔙 Ritorna al menu magazzino", callback_data='main_storage')]]),

            "custom_new_product_storage": InlineKeyboardMarkup(
                [[InlineKeyboardButton("🔙 Ritorna al menu magazzino", callback_data='main_storage')]]),

            "acquire_product": InlineKeyboardMarkup(
                [[InlineKeyboardButton("✔ Conferma", callback_data='acquire_price_product')],
                 [InlineKeyboardButton("🔙 Torna indietro", callback_data='select_new_product')]]),

            "acquire_price_product": InlineKeyboardMarkup(
                [[InlineKeyboardButton("🔙 Torna indietro", callback_data='select_new_product')]]),

            "acquire_price": InlineKeyboardMarkup(
                [[InlineKeyboardButton("✔ Conferma", callback_data='product_added')],
                 [InlineKeyboardButton("🔙 Torna indietro", callback_data='acquire_price_product')]]),

        }

        self.WARNING_KEYBOARDS = {

            "select_new_product": InlineKeyboardMarkup(
                [[InlineKeyboardButton("🔙 Ritorna al menu magazzino", callback_data='main_storage')]]),

            "acquire_product": InlineKeyboardMarkup(
                [[InlineKeyboardButton("🔙 Torna indietro", callback_data='select_new_product')]]),

            "acquire_price_product": InlineKeyboardMarkup(
                [[InlineKeyboardButton("🔙 Torna indietro", callback_data='select_new_product')]]),

            "acquire_price": InlineKeyboardMarkup(
                [[InlineKeyboardButton("🔙 Torna indietro", callback_data='select_new_product')]]),

        }

        self.WARNING_MESSAGES = {
        }

        self.ERROR_MESSAGES = {

            "acquire_product": "Nome prodotto già esistente! Cambialo",

            "acquire_price": "Inserire un importo numerico valido!",
        }

    def set_product_to_store(self, product_to_store: str):
        self.product_params["acquire_product"] = product_to_store

    async def start_conversation(self, update: Update, context: ContextTypes.DEFAULT_TYPE, query=None,
                                 current_batch: str = None):
        self.query = query
        self.current_batch = current_batch
        username = query.from_user.first_name
        admin_who_makes_the_query = query.from_user.id
        auletta = GetNomeAuletta(GetMyAuletta(admin_who_makes_the_query))
        self.product_params["auletta"] = auletta

        buttons = []
        for prodotto in GetProdottiNonAssociati(GetMyAuletta(admin_who_makes_the_query)):
            button = InlineKeyboardButton(text=prodotto.descrizione, callback_data=prodotto.descrizione)
            buttons.append([button])

        buttons.append([InlineKeyboardButton("Crea Nuovo ➕", callback_data='custom_new_product_storage')])
        buttons.append([InlineKeyboardButton("🔙 Torna indietro", callback_data='main_storage')])
        self.UNREGISTERED_PRODUCTS = InlineKeyboardMarkup(buttons)
        if len(buttons) > 2:
            await query.edit_message_text(f"Ciao {username}, di seguito trovi tutti i prodotti non presenti nella "
                                          f"tua Auletta ({auletta}).\n"
                                          f"Seleziona uno di essi per aggiungerlo oppure creane uno nuovo con "
                                          f"l'apposito bottone 😊",
                                          reply_markup=self.UNREGISTERED_PRODUCTS)
        else:
            await query.edit_message_text(f"Ciao {username}, la tua Auletta ({auletta}) ha già tutti i prodotti!"
                                          f"Quindi creane uno nuovo con l'apposito bottone 😊",
                                          reply_markup=self.UNREGISTERED_PRODUCTS)

    async def forward_conversation(self, query, context: ContextTypes.DEFAULT_TYPE, current_batch: str):
        self.query = query
        self.current_batch = current_batch
        await query.edit_message_text(self.INTRO_MESSAGES[current_batch], reply_markup=self.KEYBOARDS[current_batch])

    async def acquire_conversation_param(self, context: ContextTypes.DEFAULT_TYPE, previous_batch: str,
                                         current_batch: str, next_batch: str, chat_id: int, message_id: int,
                                         typed_string: str, flag: bool, flag2: bool = None, typed_num: float = None):

        await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
        if flag:
            if flag2:
                query = self.query
                await query.edit_message_text(text=self.WARNING_MESSAGES[current_batch],
                                              reply_markup=self.WARNING_KEYBOARDS[current_batch])
            else:
                query = self.query
                self.product_params[current_batch] = typed_string if typed_num is None else typed_num
                self.current_batch = current_batch
                await query.edit_message_text(self.text_to_send(current_batch=current_batch,
                                                                optional_param=typed_string,
                                                                another_optional_param=typed_num),
                                              reply_markup=self.KEYBOARDS[current_batch])

        else:
            query = self.query
            await query.edit_message_text(text=self.ERROR_MESSAGES[current_batch],
                                          reply_markup=self.WARNING_KEYBOARDS[current_batch])

    async def end_conversation(self, update: Update, context: ContextTypes.DEFAULT_TYPE, query=None):
        auletta = self.product_params["auletta"]
        product_name = self.product_params["acquire_product"]
        product_price = self.product_params["acquire_price"]

        if product_price == 0:
            # Fast end
            product_price = QuantitaECosto(GetIDProdotto(product_name), GetAuletta(auletta=auletta)).costo

        AssegnaProdotto(nomeAuletta=auletta, nomeProdotto=product_name, costo=product_price, isVisible=True)

        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Torna al menu magazzino",
                                                               callback_data='main_storage')]])
        await query.edit_message_text(
            f"{product_name} al costo di {product_price}, aggiunto all'Auletta {auletta} correttamente!",
            reply_markup=keyboard)

        await context.bot.send_message(chat_id=GetIdGruppoTelegram(GetAuletta(auletta)),
                                       text=f'Ciao ragazzi, {GetUsername(query.from_user.id)} ha aggiunto un prodotto '
                                            f'avente i seguenti dati\n'
                                            f"Nome -> {product_name}\n"
                                            f"Prezzo   -> {product_price}\n"
                                            f"Auletta  -> {auletta}")

        self.current_batch = ""

    def text_to_send(self, optional_param: str = None, current_batch: str = None,
                     another_optional_param: str = None) -> str:
        """Base on the current batch the message to send need to be manipulated"""
        if current_batch == "acquire_product":
            return f"{self.INTRO_MESSAGES[current_batch]} {optional_param}?"
        elif current_batch == "acquire_price":
            return f"{self.INTRO_MESSAGES[current_batch]} {another_optional_param}?"

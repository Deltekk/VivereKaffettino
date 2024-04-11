from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from telegram.ext import ContextTypes
from Modules.Bot.Utility import *
from ..Shared.Query import GetIdTelegram, CheckUsernameExists, GetIsVerified, GetIsAdmin, getGender, GetUnverifiedUsers
from Modules.Shared.Query import InsertUser, GetAulette, incrementaSaldo, SetAdminDB, InsertUser, GetUsername, \
    assignCard, GetUnverifiedUsers, SetIsVerified
from Modules.Bot.ShowBalance import ShowBalance
from Modules.Bot.Start import Start
from Modules.Bot.Stop import Stop
from Modules.Bot.UserInfo import Info
import re


async def button_callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ogni qual volta viene premuto un bottone del menù"""

    if "first_start" in context.user_data:
        context.user_data['first_start'] = False

    query = update.callback_query

    match query.data:

        case 'back_main_menu':
            # Interrompo eventuali conversazioni in corso
            for action in ACTIONS:
                if action in context.user_data:
                    context.user_data.pop(action)
            await Start(update, context)

        case 'stop':
            # Interrompo eventuali conversazioni in corso
            for action in ACTIONS:
                if action in context.user_data:
                    context.user_data.pop(action)
            await Stop(update, context)

        case "info":
            await Info(update, context)

        case 'saldo':
            await ShowBalance(update, context)

        case "registra":
            # Elimino l'eventuale conversazione nel caso premo il bottone per tornare indietro
            if "acquire_age" in context.user_data:
                context.user_data.pop('acquire_age')
            # Creo una nuova conversazione
            context.user_data['acquire_username_toregister'] = query
            keyboard = InlineKeyboardMarkup(buttons_dict["back_main_menu"])
            await query.edit_message_text(
                f"Digita l'username rispettando lo stardard Unipa con iniziali grandi.\nEs: Massimo.Midiri03",
                reply_markup=keyboard)

        case "age":
            # Elimino l'eventuale conversazione nel caso premo il bottone per tornare indietro
            if "gender" in context.user_data:
                context.user_data.pop('gender')
            # Creo una nuova conversazione
            context.user_data["acquire_age"] = query
            keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Torna indietro", callback_data='registra')]])
            await query.edit_message_text(
                f"Digita la tua data di nascita rispettando il formato dell'esempio per favore.\nEs: 11/09/2001",
                reply_markup=keyboard)

        case "selecting_gender":
            # Elimino l'eventuale conversazione nel caso premo il bottone per tornare indietro
            if "gender" in context.user_data:
                context.user_data.pop('gender')
            # Creo una nuova conversazione
            keyboard = InlineKeyboardMarkup(buttons_dict["selecting_gender"])
            await query.edit_message_text(text=f"Adesso seleziona il tuo genere per favore", reply_markup=keyboard)

        case gender_selezionato if gender_selezionato in {'donna', 'uomo', 'altro'}:
            keyboard = InlineKeyboardMarkup(buttons_dict["done_selecting_gender"])
            context.user_data["gender"] = query.data
            await query.edit_message_text(text=f"Hai selezionato {query.data.upper()}, confermi?",
                                          reply_markup=keyboard)

        case "selecting_auletta_registra":
            buttons = []
            for auletta in GetAulette():
                auletta = str(auletta).split()
                button = InlineKeyboardButton(text=auletta[1], callback_data=auletta[1])
                buttons.append([button])
            buttons.append([InlineKeyboardButton("🔙 Torna indietro", callback_data='selecting_gender')])
            keyboard = InlineKeyboardMarkup(buttons)
            await query.edit_message_text(text=f"Seleziona la tua Auletta di appartenenza",
                                          reply_markup=keyboard)

        case auletta_selezionata if auletta_selezionata in {str(auletta).split()[1] for auletta in GetAulette()}:
            context.user_data["auletta"] = query.data
            Inserisci_Utente(context)
            buttons = [[InlineKeyboardButton("🔙 Ritorna al menu principale", callback_data='back_main_menu')]]
            keyboard = InlineKeyboardMarkup(buttons)
            await query.edit_message_text(
                text=f"{context.user_data['username']} benvenut{GENDER_DICT[context.user_data['gender']]} in Vivere Kaffettino!",
                reply_markup=keyboard)
            context.user_data.pop("username")
            context.user_data.pop("username_id")
            context.user_data.pop("gender")
            context.user_data.pop("dataNascita")
            context.user_data.pop("auletta")

        case 'ricarica':
            context.user_data['acquire_amount_tocharge'] = query
            buttons = [[InlineKeyboardButton("❌ Annulla", callback_data='back_main_menu')]]
            keyboard = InlineKeyboardMarkup(buttons)
            await query.edit_message_text(f"Digita l'username dell'utente che vuole ricaricare", reply_markup=keyboard)

        case "done_ricarica":
            buttons = [[InlineKeyboardButton("🔙 Ritorna al menu principale", callback_data='back_main_menu')]]
            keyboard = InlineKeyboardMarkup(buttons)
            await context.bot.delete_message(chat_id=context.user_data["chat_id"], message_id=context.user_data["message_id"])
            incrementaSaldo(context.user_data['username'], context.user_data["amout"])
            await query.edit_message_text(
                text=f"Ricarica a {context.user_data['username']} effettuata!\nTorna pure al menu principale",
                reply_markup=keyboard)
            context.user_data.pop("validate_amount_tocharge")
            context.user_data.pop("username")
            context.user_data.pop("chat_id")
            context.user_data.pop("message_id")
            context.user_data.pop("amount")

        case "admin":
            keyboard = InlineKeyboardMarkup(buttons_dict["admin"])
            await query.edit_message_text(f"GESTIONE ADMIN", reply_markup=keyboard)

        case "add_admin":
            context.user_data['acquire_user_tomake_admin'] = query
            buttons = [[InlineKeyboardButton("❌ Annulla", callback_data='admin')]]
            keyboard = InlineKeyboardMarkup(buttons)
            await query.edit_message_text(f"Digita l'username dell'utente da far diventare admin",
                                          reply_markup=keyboard)

        case "remove_admin":
            context.user_data['acquire_user_toremove_from_admin'] = query
            buttons = [[InlineKeyboardButton("❌ Annulla", callback_data='admin')]]
            keyboard = InlineKeyboardMarkup(buttons)
            await query.edit_message_text(f"Digita l'username dell'utente da rimuovere dagli admin",
                                          reply_markup=keyboard)

        case "acquire_user_toverify":
            buttons = list()
            for id_auletta in range(len(GetAulette())):
                for utente in GetUnverifiedUsers(id_auletta+1):
                    button = InlineKeyboardButton(text=utente[0], callback_data=utente[0])
                    buttons.append([button])
            buttons.append([InlineKeyboardButton("🔙 Torna indietro", callback_data='admin')])
            keyboard = InlineKeyboardMarkup(buttons)
            if len(buttons) == 1:
                await query.edit_message_text(f"Non ci sono utenti da verificare", reply_markup=keyboard)
            else:
                await query.edit_message_text(f"Scegli chi abilitare", reply_markup=keyboard)

        case utente_selezionato if utente_selezionato in {utente[0] for id_auletta in range(len(GetAulette())) for utente in GetUnverifiedUsers(id_auletta+1)}:
            keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("✔ Conferma", callback_data='acquire_card_number')],
                                             [InlineKeyboardButton("🔙 Torna indietro", callback_data='acquire_user_toverify')]])

            await query.edit_message_text(f"Hai scelto {utente_selezionato}, confermi?", reply_markup=keyboard)
            context.user_data["user_toverify"] = utente_selezionato


        case "acquire_card_number":
            context.user_data["acquire_card_number"] = query
            buttons = [[InlineKeyboardButton("🔙 Torna indietro", callback_data='acquire_user_toverify')]]
            keyboard = InlineKeyboardMarkup(buttons)
            await query.edit_message_text(f"Digita l'ID CARD da assegnare all'utente", reply_markup=keyboard)

        case "acquired_card":
            # Completa la verifica dell'utente una volta inserito il numero della CARD
            assignCard(GetIdTelegram(context.user_data['user_toverify']), context.user_data['idCard'])
            idTelegram = GetIdTelegram(username=context.user_data['user_toverify'])
            gender = getGender(idTelegram=idTelegram)

            SetIsVerified(GetIdTelegram(context.user_data["user_toverify"]))

            keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Ritorna al menu admin", callback_data='admin')]])
            await query.edit_message_text(
                text=f"L'utente {context.user_data['user_toverify']} è stato verificato correttamente!",
                reply_markup=keyboard)
            # Avviso l'utente che è stato verificato
            await context.bot.send_message(chat_id=GetIdTelegram(context.user_data['user_toverify']),
                                           text=f'{context.user_data["user_toverify"]}, sei stat{DB_GENDER_DICT[gender]} abilitat{DB_GENDER_DICT[gender]} ad usare Vivere Kaffettino.\n\nVieni in auletta per ritirare la card!\n\nPremi /start per iniziare e goditi i tuoi caffè! :)')
            context.user_data.pop("acquire_card_number")
            context.user_data.pop("idCard")
            context.user_data.pop("user_toverify")



        case "storage":
            # TODO: Sotto menu per lo storage e relative comunicazioni con il DB
            buttons = [[InlineKeyboardButton("Visualizza magazzino 🗄", callback_data='see_storage')],
                       [InlineKeyboardButton("Incrementa scorta 🟩", callback_data='add_storage')],
                       [InlineKeyboardButton("Rimuovi Prodotto 🟥", callback_data='remove_storage')],
                       [InlineKeyboardButton("Aggiungi Prodotto ➕", callback_data='new_storage')],
                       [InlineKeyboardButton("🔙 Ritorna al menu principale", callback_data='back_main_menu')]]
            keyboard = InlineKeyboardMarkup(buttons)
            await query.edit_message_text(f"GESTIONE MAGAZZINO", reply_markup=keyboard)


async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Quando viene scritto qualcosa in chat"""

    if "acquire_username_toregister" in context.user_data:
        username = update.message.text
        chat_id = update.message.chat_id
        message_id = update.message.message_id
        await acquire_username_toregister(username, chat_id, message_id, context)


    elif "acquire_age" in context.user_data:
        age = update.message.text
        chat_id = update.message.chat_id
        message_id = update.message.message_id
        await acquire_age(age, chat_id, message_id, context)


    elif "acquire_amount_tocharge" in context.user_data:
        username = update.message.text
        chat_id = update.message.chat_id
        message_id = update.message.message_id
        await acquire_amount_tocharge(username, chat_id, message_id, context)


    elif "validate_amount_tocharge" in context.user_data:
        amount = update.message.text
        chat_id = update.message.chat_id
        message_id = update.message.message_id
        await validate_amount_tocharge(amount, chat_id, message_id, context)


    elif "acquire_user_tomake_admin" in context.user_data:
        username = update.message.text
        chat_id = update.message.chat_id
        message_id = update.message.message_id
        await acquire_user_tomake_admin(username, chat_id, message_id, context)


    elif "acquire_user_toremove_from_admin" in context.user_data:
        username = update.message.text
        chat_id = update.message.chat_id
        message_id = update.message.message_id
        await acquire_user_toremove_from_admin(username, chat_id, message_id, context)


    elif "acquire_user_toverify" in context.user_data:
        username = update.message.text
        chat_id = update.message.chat_id
        message_id = update.message.message_id
        await acquire_user_toverify(username, chat_id, message_id, context)


    elif "acquire_card_number" in context.user_data:
        idCard = update.message.text
        chat_id = update.message.chat_id
        message_id = update.message.message_id
        await acquire_card_number(idCard, chat_id, message_id, context)


    else:
        await context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)


async def acquire_username_toregister(username: str, chat_id: int, message_id: int, context: ContextTypes.DEFAULT_TYPE):
    if check_regex_username(username):
        await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
        keyboard = InlineKeyboardMarkup(buttons_dict["correct_acquire_username_toregister"])
        query = context.user_data["acquire_username_toregister"]
        context.user_data["username"] = username
        context.user_data["username_id"] = chat_id
        await query.edit_message_text(text=f"Hai scritto {username}, confermi?", reply_markup=keyboard)
        # Esco dalla conversazione
        context.user_data.pop("acquire_username_toregister")
    else:
        await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
        query = context.user_data["acquire_username_toregister"]
        keyboard = InlineKeyboardMarkup(buttons_dict["wrong_acquire_username_toregister"])
        await query.edit_message_text(
            f"Hai digitato un username che non rispetta lo stardard Unipa, riprova.\nEs: Massimo.Midiri03",
            reply_markup=keyboard)


async def acquire_age(age: str, chat_id: int, message_id: int, context: ContextTypes.DEFAULT_TYPE):
    if check_regex_age(age):
        await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
        keyboard = InlineKeyboardMarkup(buttons_dict["correct_acquire_age"])
        query = context.user_data["acquire_age"]
        context.user_data["dataNascita"] = age
        await query.edit_message_text(text=f"Hai scritto {age}, confermi?", reply_markup=keyboard)
        # Esco dalla conversazione
        context.user_data.pop("acquire_age")
    else:
        await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
        query = context.user_data["acquire_age"]
        keyboard = InlineKeyboardMarkup(buttons_dict["back_main_menu"])
        await query.edit_message_text(
            f"Hai digitato una data di nascita che non rispetta lo stardard, riprova.\nEs: 11/09/2001",
            reply_markup=keyboard)


async def acquire_amount_tocharge(username: str, chat_id: int, message_id: int, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.delete_message(chat_id=chat_id, message_id=message_id)

    buttons = [[InlineKeyboardButton("❌ Annulla", callback_data='back_main_menu')]]
    keyboard = InlineKeyboardMarkup(buttons)
    query = context.user_data["acquire_amount_tocharge"]
    if GetIdTelegram(username=username) != "None":
        context.user_data["validate_amount_tocharge"] = query
        context.user_data["username"] = username
        await query.edit_message_text(text="Digita l'importo da ricaricare", reply_markup=keyboard)
        context.user_data.pop("acquire_amount_tocharge")
    else:
        await query.edit_message_text(text="Utente non trovato riprova oppure ritorna al menu principale",
                                      reply_markup=keyboard)


async def validate_amount_tocharge(amount: str, chat_id: int, message_id: int, context: ContextTypes.DEFAULT_TYPE):
    query = context.user_data["validate_amount_tocharge"]
    try:
        amount = float(amount)
    except ValueError:
        buttons = [[InlineKeyboardButton("❌ Annulla", callback_data='back_main_menu')]]
        keyboard = InlineKeyboardMarkup(buttons)
        await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
        await query.edit_message_text(text="Inserire un importo numerico valido!",
                                      reply_markup=keyboard)
    else:
        if amount <= 0:
            buttons = [[InlineKeyboardButton("❌ Annulla", callback_data='back_main_menu')]]
            keyboard = InlineKeyboardMarkup(buttons)
            await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
            await query.edit_message_text(text="La ricarica deve essere positiva!",
                                          reply_markup=keyboard)
        else:
            keyboard = InlineKeyboardMarkup(buttons_dict["validate_amount_tocharge"])
            context.user_data["amout"] = amount
            context.user_data["chat_id"] = chat_id
            context.user_data["message_id"] = message_id
            await query.edit_message_text(text=f"Sicuro di voler confermare {amount}?", reply_markup=keyboard)


async def acquire_user_tomake_admin(username: str, chat_id: int, message_id: int, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
    query = context.user_data["acquire_user_tomake_admin"]
    if GetIdTelegram(username=username) != "None":
        if GetIsAdmin(GetIdTelegram(username=username)):
            buttons = [[InlineKeyboardButton("🔙 Ritorna al menu principale", callback_data='back_main_menu')]]
            keyboard = InlineKeyboardMarkup(buttons)
            await query.edit_message_text(text=f"L'utente {username} è già un Admin",
                                          reply_markup=keyboard)
            context.user_data.pop("acquire_user_tomake_admin")
        else:
            SetAdminDB(GetIdTelegram(username=username), True)
            buttons = [[InlineKeyboardButton("🔙 Ritorna al menu principale", callback_data='back_main_menu')]]
            keyboard = InlineKeyboardMarkup(buttons)
            await query.edit_message_text(text=f"Ok, l'utente {username} è stato promosso ad Admin",
                                          reply_markup=keyboard)
            context.user_data.pop("acquire_user_tomake_admin")
    else:
        buttons = [[InlineKeyboardButton("❌ Annulla", callback_data='admin')]]
        keyboard = InlineKeyboardMarkup(buttons)
        await query.edit_message_text(text="Utente non trovato riprova oppure annulla",
                                      reply_markup=keyboard)


async def acquire_user_toremove_from_admin(username: str, chat_id: int, message_id: int, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
    query = context.user_data["acquire_user_toremove_from_admin"]
    if GetIdTelegram(username=username) != "None":
        if GetIsAdmin(GetIdTelegram(username=username)):
            SetAdminDB(GetIdTelegram(username=username), False)
            buttons = [[InlineKeyboardButton("🔙 Ritorna al menu principale", callback_data='back_main_menu')]]
            keyboard = InlineKeyboardMarkup(buttons)
            await query.edit_message_text(text=f"Ok, l'utente {username} è stato tolto dagli Admin",
                                          reply_markup=keyboard)
            context.user_data.pop("acquire_user_toremove_from_admin")
        else:
            buttons = [[InlineKeyboardButton("❌ Annulla", callback_data='admin')]]
            keyboard = InlineKeyboardMarkup(buttons)
            await query.edit_message_text(text="L'utente non è un admin, riprova oppure annulla",
                                          reply_markup=keyboard)
    else:
        buttons = [[InlineKeyboardButton("❌ Annulla", callback_data='admin')]]
        keyboard = InlineKeyboardMarkup(buttons)
        await query.edit_message_text(text="Utente non trovato riprova oppure annulla",
                                      reply_markup=keyboard)


async def acquire_user_toverify(username: str, chat_id: int, message_id: int, context: ContextTypes.DEFAULT_TYPE):
    """Acquisisco il nome utente che deve essere verificato"""
    await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
    query = context.user_data["acquire_user_toverify"]

    if GetIdTelegram(username) != "None":
        buttons = [[InlineKeyboardButton("✔ Conferma", callback_data='acquire_card_number')],
                   [InlineKeyboardButton("❌ Annulla", callback_data='acquire_user_toverify')]]
        keyboard = InlineKeyboardMarkup(buttons)
        context.user_data["username"] = username
        context.user_data.pop("acquire_user_toverify")
        await query.edit_message_text(text=f"Sicuro di voler confermare {username}?", reply_markup=keyboard)
    else:
        buttons = [[InlineKeyboardButton("❌ Annulla", callback_data='back_main_menu')]]
        keyboard = InlineKeyboardMarkup(buttons)
        await query.edit_message_text(text="Utente non trovato, riprova o ritorna al menu principale",
                                      reply_markup=keyboard)


async def acquire_card_number(idCard: str, chat_id: int, message_id: int, context: ContextTypes.DEFAULT_TYPE):
    """Acquisisco il numero della CARD"""
    await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
    query = context.user_data["acquire_card_number"]

    if idCard.isdigit():
        keyboard = InlineKeyboardMarkup(buttons_dict["acquire_card_number"])
        context.user_data["idCard"] = idCard
        await query.edit_message_text(text=f"Sicuro di voler confermare {context.user_data['user_toverify']} con idCard: {idCard}?", reply_markup=keyboard)
    else:
        buttons = [[InlineKeyboardButton("🔙 Torna indietro all'username", callback_data='verify_user')]]
        keyboard = InlineKeyboardMarkup(buttons)
        await query.edit_message_text(text="ID CARD non valido, inserire un valore strettamente numerico!",
                                      reply_markup=keyboard)


def Inserisci_Utente(context: ContextTypes.DEFAULT_TYPE):
    """Memorizza nel DB e avvisa gli admin"""
    InsertUser(idTelegram=context.user_data["username_id"], auletta=context.user_data["auletta"],
               genere=convertToGenderDB(context.user_data["gender"]), dataNascita=context.user_data["dataNascita"],
               username=context.user_data["username"])

    # TODO: Quando un utente crea il proprio profilo, viene mandato un messaggio al
    #      gruppo degli amministratori in base all'auletta di afferenza.


def check_regex_username(username: str) -> bool:
    """Controlla se l'username dell'utente rispetta lo standard Unipa 'Nome.Cognome{int}{int}' """
    pattern = r"^[A-Z][a-z-A-Z]+\.[A-Z][a-z-A-Z]+(([1-9][1-9])|0[1-9]|[1-9]0)?$"
    return re.match(pattern, username)


def check_regex_age(age: str) -> bool:
    """Controlla se l'età inserita ha il formato corretto"""
    pattern = r"^(0[1-9]|[12][0-9]|3[01])\/(0[1-9]|1[0-2])\/((19|20)\d\d)$"
    return re.match(pattern, age)


def convertToGenderDB(gender: str) -> str:
    """Ritorna solo la prima lettera del genere passato come parametro"""
    return gender[0].upper()

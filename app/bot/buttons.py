import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from app.bot.exploration import explorar_location

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    logger.info(f"User {user.id} started the bot.")

    keyboard = [
        [InlineKeyboardButton("Explorar Floresta", callback_data='explorar_floresta')],
        [InlineKeyboardButton("Explorar Montanha", callback_data='explorar_montanha')],
        [InlineKeyboardButton("Explorar Caverna", callback_data='explorar_caverna')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = f"Olá, Mestre pokemon {user.first_name}! Vamos capturar pokemons.\nEscolha uma opção para explorar:"
    await update.message.reply_text(message, reply_markup=reply_markup)

async def continue_exploration(query, context: ContextTypes.DEFAULT_TYPE, action: str) -> None:
    user = query.from_user
    logger.info(f"User {user.id} continue exploration.")

    keyboard = [
        [InlineKeyboardButton("Explorar Floresta", callback_data='explorar_floresta')],
        [InlineKeyboardButton("Explorar Montanha", callback_data='explorar_montanha')],
        [InlineKeyboardButton("Explorar Caverna", callback_data='explorar_caverna')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if action == 'correu':
        message = f"Você fugiu do Pokémon!"
    elif action == 'capturou':
        message = f"Escolha uma opção para explorar:"
    
    await query.message.edit_text(message, reply_markup=reply_markup)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    if query.data.startswith('explorar_'):
        location = query.data.split('_')[1]
        await explorar_location(query, context, location)
    elif query.data.startswith('capturar_'):
        _, pokemon_id, pokemon_name = query.data.split('_')
        from app.bot.capture import capturar_pokemon  # Importar localmente para evitar importação circular
        await capturar_pokemon(query, context, pokemon_id, pokemon_name)
    elif query.data == 'correr':
        await continue_exploration(query, context, 'correu')
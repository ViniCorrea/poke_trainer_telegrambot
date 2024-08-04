import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
import random
import asyncio
from app.config import settings

logger = logging.getLogger(__name__)

async def capturar_pokemon(query, context, pokemon_id: str, pokemon_name: str) -> None:
    user = query.from_user
    logger.info(f"User {user.id} is trying to capture Pokémon with ID: {pokemon_id}")

    pokeball_gif_url  = "https://media.giphy.com/media/LUCh9XIvVSAHBlqgsa/giphy.gif" 
    pokeball_message = await query.message.reply_animation(pokeball_gif_url)

    await asyncio.sleep(settings.WAIT_TIME_TO_CAPTURE)

    if random.randint(1, 100) <= settings.CAPTURE_SUCCESS_RATE:
        message = (
            f"Parabéns, {user.first_name}! Você capturou o Pokémon <b>{pokemon_name}</b>!"
        )
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Ver Detalhes", url=f'https://www.pokemon.com/br/pokedex/{pokemon_name}')]
        ])
        await query.message.reply_text(message, parse_mode=ParseMode.HTML, reply_markup=keyboard)
    else:
        message = f"Que pena, {user.first_name}. O <b>{pokemon_name}</b> fugiu!"
        await query.message.reply_text(message, parse_mode=ParseMode.HTML)

    await pokeball_message.delete()  # Remove a mensagem da Pokebola

    from app.bot.buttons import continue_exploration  # Importar localmente para evitar importação circular
    await continue_exploration(query, context, 'capturou')  # Volta para o estado inicial

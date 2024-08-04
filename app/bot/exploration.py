import logging
import asyncio
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
import httpx
from app.bot.utils import TYPE_COLORS
from app.config import settings

logger = logging.getLogger(__name__)

# Defina os URLs dos GIFs para cada localização
GIFS = {
    "caverna": "https://media.giphy.com/media/8UYMQ5MCmuqXu/giphy.gif",
    "montanha": "https://media.giphy.com/media/ZdDKemV0IM0De/giphy.gif",
    "floresta": "https://media.giphy.com/media/yjGjYgx29q8VBrO3pq/giphy.gif",
}

async def explorar_location(query, context, location: str) -> None:
    user = query.from_user
    logger.info(f"User {user.id} issued explorar with location: {location}")

    # Enviar o GIF animado correspondente à localização
    loading_gif = GIFS.get(location, "https://media.giphy.com/media/3o7qE1YN7aBOFPRw8E/giphy.gif")  # GIF padrão
    loading_message = await query.message.reply_animation(animation=loading_gif)

    await asyncio.sleep(settings.WAIT_TIME_TO_FIND_A_POKEMON)  # Espera por 3 segundos

    try:
        logger.info(f"Sending request to API: {settings.PUBLIC_URL}/api/pokemon/{location}")
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{settings.PUBLIC_URL}/api/pokemon/{location}")
            logger.info(f"API request sent. Status code: {response.status_code}")
            response.raise_for_status()
            data = response.json()
        logger.info(f"API response received: {data}")

        if "name" in data:
            logger.info(f"User {user.id} found a Pokémon: {data['name']}")

            pokemon_type = data["type"]
            background_color = TYPE_COLORS.get(pokemon_type, "#FFFFFF")

            message = (
                f"<b>{data['name']}</b>\n"
                f"Altura: {data['height']} dm\n"
                f"Peso: {data['weight']} hg\n"
                f"<a href='{data['gif']}'>&#8205;</a>"  # Força o preview do GIF
            )

            keyboard = [
                [InlineKeyboardButton("Capturar", callback_data=f'capturar_{data["id"]}_{data["name"]}'),
                 InlineKeyboardButton("Correr", callback_data='correr')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await query.message.reply_text(
                message, parse_mode=ParseMode.HTML, reply_markup=reply_markup
            )
        else:
            logger.info(f"User {user.id} found nothing.")
            await query.message.reply_text("Nada encontrado.")
        
        # Remove o GIF animado após exibir o resultado
        await loading_message.delete()

    except httpx.HTTPStatusError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")  # Log HTTP errors
        await query.message.reply_text(f"Erro HTTP: {http_err}")
    except Exception as err:
        logger.error(f"Other error occurred: {err}")  # Log any other errors
        await query.message.reply_text(f"Erro: {err}")

        # Remove o GIF animado em caso de erro
        await loading_message.delete()
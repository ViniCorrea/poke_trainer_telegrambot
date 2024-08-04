from fastapi import APIRouter, HTTPException
import pokebase as pb
from random import randint
import logging
from app.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/pokemon/{location}")
def explore_location(location: str):
    logger.info(f"Exploring location: {location}")
    if randint(1, 100) <= settings.FIND_POKEMON_RATE:
        try:
            logger.info(f"Random condition met, fetching a Pokémon.")
            pokemon_id = randint(1, settings.MAX_POKEMON_ID)
            pokemon = pb.pokemon(pokemon_id)
            pokemon_type = pokemon.types[0].type.name  # Assume o primeiro tipo
            
            pokemon_gif = pokemon.sprites.versions.generation_v.black_white.animated.front_default
            if not pokemon_gif:
                pokemon_gif = pokemon.sprites.front_default
            
            response = {
                "id": pokemon_id,
                "name": pokemon.name,
                "sprite": pokemon.sprites.front_default,
                "gif": pokemon_gif,
                "height": pokemon.height,
                "weight": pokemon.weight,
                "type": pokemon_type
            }
            
            logger.info(f"Found Pokémon: {response}")
            return response
        except Exception as e:
            logger.error(f"Error fetching Pokémon: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    else:
        logger.info("No Pokémon found.")
        return {"message": "Nada encontrado."}

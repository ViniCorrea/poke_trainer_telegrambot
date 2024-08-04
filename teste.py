from random import randint
from fastapi import FastAPI, HTTPException
import pokebase as pb
import logging

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/test")
def test_endpoint():
    logger.info("Test endpoint called.")
    return {"message": "API is working"}

@app.get("/pokemon/{location}")
def explore_location(location: str):
    logger.info(f"Exploring location: {location}")
    if randint(1, 10) > 7:
        try:
            pokemon_id = randint(1, 898)
            pokemon = pb.pokemon(pokemon_id)
            response = {
                "name": pokemon.name,
                "sprite": pokemon.sprites.front_default,
                "height": pokemon.height,
                "weight": pokemon.weight
            }
            logger.info(f"Found Pokémon: {response}")
            return response
        except Exception as e:
            logger.error(f"Error fetching Pokémon: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    else:
        logger.info("No Pokémon found.")
        return {"message": "Nada encontrado."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

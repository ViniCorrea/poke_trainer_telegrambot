import logging
import signal
import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from app.api.endpoints import router as api_router
from app.bot.bot import start_bot, stop_bot

logging.basicConfig(level=logging.INFO)

@asynccontextmanager
async def app_lifespan(app: FastAPI):
    loop = asyncio.get_event_loop()
    stop_event = asyncio.Event()

    def shutdown():
        logging.info("Received shutdown signal")
        stop_event.set()

    signal.signal(signal.SIGINT, lambda s, f: shutdown())
    signal.signal(signal.SIGTERM, lambda s, f: shutdown())

    logging.info("Starting bot...")
    await start_bot()
    yield
    logging.info("Stopping bot...")
    await stop_bot()
    await stop_event.wait()

app = FastAPI(lifespan=app_lifespan)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")
#app.mount("/static", StaticFiles(directory="static"), name="static")

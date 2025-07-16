import json
from typing import List

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from starlette.responses import FileResponse

from .game import get_magic_number, play_mash
from .llm import generate_mash_options

load_dotenv()

app = FastAPI()


# Pydantic gives us request and response validation (dataclasses do not)
class Category(BaseModel):
    name: str
    options: List[str]


class GameData(BaseModel):
    categories: List[Category]
    magic_number: int


class GameOptions(BaseModel):
    theme: str
    platform: str
    api_key: str | None = None


@app.post("/api/generate_options")
async def generate_options(game_options: GameOptions):
    try:
        options = generate_mash_options(
            game_options.theme, platform=game_options.platform, api_key=game_options.api_key
        )
        return {"options": options}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM generation failed: {e}")


@app.get("/api/magic_number")
def read_magic_number():
    return {"magic_number": get_magic_number()}


@app.post("/api/play")
def play_game(game_data: GameData):
    game_state = play_mash([cat.model_dump() for cat in game_data.categories], game_data.magic_number)
    return game_state


app.mount("/static", StaticFiles(directory="frontend/build/static"), name="static")


@app.get("/")
async def read_index():
    return FileResponse("frontend/build/index.html")

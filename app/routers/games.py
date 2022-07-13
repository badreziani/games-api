from fastapi import status, HTTPException, APIRouter
from .. import gsheetapi
from ..config import settings
import requests
import json

router = APIRouter()
ENDPOINT = f'https://api.airtable.com/v0/{settings.airtable_base_id}/{settings.airtable_table_name}'

headers = {
    'Authorization': f'Bearer {settings.api_key}'
}

# Fetch All Games


@router.get("/api/categories", status_code=status.HTTP_200_OK)
def fetch_all_categories():
    res = json.loads(requests.get(ENDPOINT, headers=headers).text)
    records = res.get('records')
    categories = []
    for record in records:
        record_categories = record.get('fields').get('CATEGORIES')
        if isinstance(record_categories, str):
            record_categories = record_categories.split(',')

        if record_categories:
            categories += record_categories

    categories = [{"name": item, "url": item, "category": item}
                  for item in list(set(categories))]

    return {"data": {"sort": [{"name": "newest", "url": "newest"}], "category": categories}}


# Fetch All Games
@router.get("/api/games", status_code=status.HTTP_200_OK)
async def fetch_all_games(category: str | None = None, newest: str | None = None):
    res = json.loads(requests.get(ENDPOINT, headers=headers).text)
    games = res.get('records')
    if category:
        games = [game for game in games if category in game.get(
            'fields').get('CATEGORIES')]

    if newest:
        games.sort(key=lambda x: x.get('createdTime'), reverse=True)
    return {"data": games}


# Fetch All Single Game
@router.get("/api/game/{id}", status_code=status.HTTP_200_OK)
async def fetch_single_game(id: str):
    game = json.loads(requests.get(f'{ENDPOINT}/{id}', headers=headers).text)
    return {"data": game}


@router.get("/api/games/{title}", status_code=status.HTTP_200_OK)
async def fetch_single_game_by_name(title: str):
    res = json.loads(requests.get(ENDPOINT, headers=headers).text)
    game = [g for g in res.get('records') if g.get(
        'fields').get('TITLE') == title][0]
    return {"data": game}


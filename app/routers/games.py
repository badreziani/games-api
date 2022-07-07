from fastapi import Depends, UploadFile, File, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from .. import database, schemas, models, oauth2, gsheetapi

router = APIRouter()
# Fetch All Games
@router.get("/api/categories")
def fetch_all_categories(db: Session = Depends(database.get_db)):
    categories = db.query(models.Category).all()
    return {"categories": categories}


# Fetch All Games
@router.get("/api/games")
def fetch_all_games(db: Session = Depends(database.get_db)):
    games = db.query(models.Game).all()
    return {"games": games}


# Fetch All Single Game
@router.get("/api/games/{id}", response_model=schemas.Student)
async def fetch_single_game(id: int, db: Session = Depends(database.get_db)):
    game = db.query(models.Game).filter(
        models.Game.id == id).first()

    if game is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=[{"msg": "Game not found."}])

    return game


@router.post("/api/games/update", status_code=status.HTTP_201_CREATED)
async def update_db(db: Session = Depends(database.get_db)): # current_user: int = Depends(oauth2.get_current_user)

    try:
        rows = gsheetapi.get_sheet_data()
        for row in rows:
            game = db.query(models.Game).filter(models.Game.title == row[1]).first()

            if game is None:
                print(*row)
                break
                # game = models.Game(*row)
                # db.add(game)
                # db.commit()
            else:
                pass
    except:
        raise HTTPException(
            status_code=status.HTTP_408_REQUEST_TIMEOUT, detail="Timeout.")

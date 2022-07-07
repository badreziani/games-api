from fastapi import Depends, UploadFile, File, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from .. import database, schemas, models, oauth2

router = APIRouter()

# Fetch All Games
@router.get("/api/games")
def fetch_all(db: Session = Depends(database.get_db)):
    games = db.query(models.Game).all()
    return {"games": games}

# Fetch All Single Game
@router.get("/api/games/{id}", response_model=schemas.Student)
async def fetch_single(id: int, db: Session = Depends(database.get_db)):
    game = db.query(models.Game).filter(
        models.Game.id == id).first()

    if game is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=[{"msg": "Game not found."}])

    return game


@router.post("/api/games/upload", status_code=status.HTTP_201_CREATED)
async def import_data(file: UploadFile = File(...), db: Session = Depends(database.get_db),  current_user: int = Depends(oauth2.get_current_user)):

    try:
        content = await file.read()
        decoded_content = content.decode('utf-8')
        rows = decoded_content.split("\r\n")
        rows.sort()

        for row in rows:
            data = row.split(',')

            student_exists_in_db = False if db.query(models.Student).filter(
                models.Student.cne == data[0]).first() is None else True

            if not student_exists_in_db:
                new_student = models.Student(cne=data[0], nom=data[1])
                db.add(new_student)
                db.commit()
                inserted_student = db.query(models.Student).filter(
                    models.Student.cne == data[0]).first()
                new_diplome = models.Diplome(
                    filiere=data[2], guichet=data[3], rdv=data[4], type=data[5], owner_id=inserted_student.id)
                db.add(new_diplome)
                db.commit()
            else:
                existing_student = db.query(models.Student).filter(
                    models.Student.cne == data[0]).first()

                diplome_query = db.query(models.Diplome).filter(
                    models.Diplome.owner_id == existing_student.id, models.Diplome.type == data[5])
                if diplome_query.first() is None:
                    new_diplome = models.Diplome(
                        filiere=data[2], guichet=data[3], rdv=data[4], type=data[5], owner_id=existing_student.id)
                    db.add(new_diplome)
                    commited = db.commit()
                else:
                    diplome_query = db.query(models.Diplome).filter(
                        models.Diplome.owner_id == existing_student.id, models.Diplome.type == data[5])
                    diplome_query.update(
                        {"guichet": data[3], "rdv": data[4]}, synchronize_session=False)
                    db.commit()
    except:
        raise HTTPException(
            status_code=status.HTTP_408_REQUEST_TIMEOUT, detail="Timeout.")

from urllib import response
from fastapi import Depends, status, HTTPException, APIRouter, File, UploadFile
from sqlalchemy.orm import Session
from typing import List
from .. import database, schemas, models, oauth2, utils


router = APIRouter(tags=["Super Admin"])


@router.post("/api/sa/upload", status_code=status.HTTP_201_CREATED)
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


@router.post("/api/sa/new-user", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):

    # hash the password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get('/api/sa/students/{cne}', response_model=List[schemas.Student])
async def get_student(cne: str, db: Session = Depends(database.get_db)):
    students = db.query(models.Student).filter(
        models.Student.cne.startswith(cne)).limit(8).all()
    if students is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=[{"msg": "Le CNE / Code MASSAR est introuvable."}])

    return students

# @router.get("/{id}", response_model=schemas.User)
# def get_user(id: int, db: Session = Depends(database.get_db)):
#     user = db.query(models.User).filter(models.User.id == id).first()

#     if user == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"User With ID : {id} Not Found.")
#     return user

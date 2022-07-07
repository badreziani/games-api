from datetime import datetime
from fastapi import Depends, status, HTTPException, APIRouter
from typing import List
from sqlalchemy.orm import Session

from .. import database, schemas, models, oauth2


router = APIRouter()


@router.get('/api/admin/students/{cne}', response_model=List[schemas.Student])
async def get_student(cne: str, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    students = db.query(models.Student).filter(
        models.Student.cne.startswith(cne)).limit(8).all()
    if students is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=[{"msg": "Le CNE / Code MASSAR est introuvable."}])

    return students


@router.put('/api/admin', response_model=schemas.Diplome)
async def update_student(diplome: schemas.DiplomeUpdate, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    current_user_id = current_user.id

    diplome_query = db.query(models.Diplome).filter(
        models.Diplome.id == diplome.id)
    if diplome_query.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=[{"msg": "Diplôme introuvable."}])
    else:
        diplome_query.update(
            {"operator_id": current_user_id, "date_retrait": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}, synchronize_session=False)
        db.commit()
        return diplome_query.first()


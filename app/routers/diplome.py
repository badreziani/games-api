from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from .. import database, schemas, models, oauth2


router = APIRouter()


# @router.post("/", status_code=status.HTTP_201_CREATED)
# async def vote(vote: schemas.VoteCreate, db: Session = Depends(database.get_db), user: int = Depends(oauth2.get_current_user)):

#     found_post = db.query(models.Post).filter(
#         models.Post.id == vote.post_id).first()
#     if found_post is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exists.")

#     find_vote_query = db.query(models.Vote).filter(
#         models.Vote.post_id == vote.post_id, models.Vote.user_id == user.id)

#     if vote.vote_dir == 1:
#         if find_vote_query.first() is None:
#             new_vote = models.Vote(user_id=user.id, post_id=vote.post_id)
#             db.add(new_vote)
#             db.commit()
#             return {"message": "Successfully Voted."}
#         else:
#             raise HTTPException(
#                 status_code=status.HTTP_409_CONFLICT, detail="You can't vote this post twice.")

#     else:
#         if find_vote_query.first() is None:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND, detail="Vote not found.")

#         find_vote_query.delete(synchronize_session=False)
#         db.commit()
#         return {"message": "Successfully Unvoted."}

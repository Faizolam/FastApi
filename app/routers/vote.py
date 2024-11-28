# Path will be al "/vote"
# The user id will extracted from the jwt token
# The body will contain the id of the post the user is voting on as well as the direction of the vote.
# {
# 	post_id:1432
# 	vote_dir:0
# }
# A vote direction of 1 means we want to add a vote, a direction of 0 means we want to delete the vote.

from fastapi import FastAPI, Response,status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..import schemas, database, models, oauth2
router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
#setting up schemas and db, current user
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int =Depends(oauth2.get_current_user)):
    ##If post doesn't exist and user trying to vote that post than i have to send exception 404 not foungd.
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {vote.post_id} does not exist")
    ##before create the vote check, is already exist or not
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if (vote.dir == 1): # checking no. of vote by a single user
       if found_vote:
           raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user Id: {current_user.id} has already voted on post: {vote.post_id}")
       new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
       db.add(new_vote)
       db.commit()
       return {"messsage": "successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()

        return{"message": "successfully deleted vote"}
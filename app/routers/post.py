from fastapi import FastAPI, Response,status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from sqlalchemy import func
from .. import models, schemas, oauth2
from .. database import get_db

router = APIRouter(
    prefix = "/posts",
    tags = ['Posts']
)
#***********************************get_posts**************************
# # @router.get("/")
# @router.get("/", response_model=List[schemas.Post])
# def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
#     # cursor.execute("""SELECT * FROM post""")
#     # posts=cursor.fetchall()
#     # posts = db.query(models.Post).all()
#     ##get post of owner specific or post only owner can access
#     # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
#     ## Get posts in limit given by user, max post limit is 10
#     ## Find any keyword in the post by this filter(models.Post.title.contains(search))
#     print(search)
#     posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
#     # print(limit)

#     results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id,isouter=True).group_by(models.Post.id).all()
#     print(results)

#     return results



#*******************************get_posts-v2******************************
# router = APIRouter()

# class PostWithVotes(schemas.Post):
#     votes: int
@router.get("/", response_model=List[schemas.PostWithVotes])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    #  # Convert the results to the new model
    # posts_with_votes = [schemas.PostWithVotes(post=post, votes=votes) for post, votes in posts]

    # Convert the results to the new model separate keyword argument
    posts_with_votes = [
        schemas.PostWithVotes(id=post.id, title=post.title, content=post.content, created_at=post.created_at, owner_id=post.owner_id, owner=post.owner,votes=votes)
        for post, votes in posts
    ]

    return posts_with_votes

#***********************************create_posts**************************
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # # cursor.execute(f"INSERT INTO post (titel, content, publidhed) VALUES ({post.title}, {post.content} )") #This way maybe chance to SQL injection attack.
    # cursor.execute("""INSERT INTO public.post(title, content, published) VALUES (%s,%s, %s ) RETURNING * """,(post.title, post.content, post.published))
    # newPost=cursor.fetchone()
    # conn.commit()

    # print(post.dict())
    # newPost=models.Post(title=post.title, content=post.content, published=post.published) #rether then that write this below
    # print(current_user.email)
    print(current_user.id)
    newPost=models.Post(owner_id=current_user.id, **post.dict())

    db.add(newPost)
    db.commit()
    db.refresh(newPost)

    return newPost
  
#***************************get_posts with id****************************
@router.get("/{id}", response_model=schemas.PostWithVotes)
def get_posts(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): #this int for input validation
    # post=db.query(models.Post).filter(models.Post.id == id).first()

    result =  db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return{'message':f"post with id: {id} was not found"}
    post,vote = result
    print(post, vote)
    posts_with_votes = schemas.PostWithVotes(id=post.id, title=post.title, content=post.content, created_at=post.created_at, owner_id=post.owner_id, owner=post.owner, votes=vote) 
    # ## Check owner is same,and only user specific post show
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    return posts_with_votes


#****************************get_posts with id-v2*************************
# @router.get("/{post_id}", response_model=schemas.PostWithVotes)
# def get_post(post_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
#     post, votes = db.query(models.Post, func.count(models.Vote.post_id).label("votes")) \
#         .filter(models.Post.id == post_id) \
#         .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True) \
#         .group_by(models.Post.id) \
#         .first()

#     if post is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    
#     post_with_votes = schemas.PostWithVotes(post=post, votes=votes)
#     return post_with_votes



#***********************************delete_post**************************
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM post WHERE id = %s RETURNING *""", (str(id),))
    # deletedPost = cursor.fetchone()
    # print(deletedPost)
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    ## check if post exist
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} dose not exist")
    ## If we did post found then check user authorized or not to delete the post
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


#***********************************update_post**************************
@router.put("/{id}", response_model = schemas.Post)
def update_post(id: int, updatedPost: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE post SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    # updatedPost = cursor.fetchone()
    # conn.commit()
    post_query=db.query(models.Post).filter(models.Post.id == id)
    # print(post_query)
    post = post_query.first()

    ## if post exist
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} dose not exist")
    
    ## If we did post found then check user authorized or not to delete the post
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    post_query.update(updatedPost.dict() , synchronize_session=False)
    db.commit()
    return post_query.first()



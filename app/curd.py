from fastapi import FastAPI, Response,status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

# Create a FastAPI instance
app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

while True:
    try:
        conn=psycopg2.connect(host="localhost", database="FastApi", user="postgres", password='Hathi8120', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was succesfull!")
        break
    except Exception as error:
        print("Connecting to database failed!")
        print("Error: ", error)
        time.sleep(2)
        
my_posts = [{"titel":"titel of post 1", "content":"content of post1", "id":1},{"titel":"favoarite foods", "content":"I like pizza","id":2}]

def find_post(id):
    for p in my_posts:
        if p['id']==id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

# Define a simple endpoint
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM post""")
    posts=cursor.fetchall()
    return {"data":posts}

@app.post("/createposts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    # cursor.execute(f"INSERT INTO post (titel, content, publidhed) VALUES ({post.title}, {post.content} )") #This way maybe chance to SQL injection attack.
    cursor.execute("""INSERT INTO public.post(title, content, published) VALUES (%s,%s, %s ) RETURNING * """,(post.title, post.content, post.published))
    newPost=cursor.fetchone()
    conn.commit()
    return {"data":newPost}
  

@app.get("/posts/{id}")
def get_posts(id: int): #this int for input validation
    cursor.execute("""SELECT * FROM post WHERE id = %s """,(str(id),)) #this is bcz sql will take str
    post=cursor.fetchone()
    conn.commit()
    print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return{'message':f"post with id: {id} was not found"}
    return {"post_detail":post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM post WHERE id = %s RETURNING *""", (str(id),))
    deletedPost = cursor.fetchone()
    print(deletedPost)
    conn.commit()
    if deletedPost == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} dose not exist")

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE post SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    updatedPost = cursor.fetchone()
    conn.commit()
    print(updatedPost)

    if updatedPost == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} dose not exist")
   
    return {'data':updatedPost}
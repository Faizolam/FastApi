# from fastapi import FastAPI, Response,status, HTTPException
# from fastapi.params import Body
# from pydantic import BaseModel
# from typing import Optional
# from random import randrange
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time

# # Create a FastAPI instance
# app = FastAPI()

# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool = True

# # while True:
# #     try:
# #         conn=psycopg2.connect(host="localhost", database="FastApi", user="postgres", password='Hathi8120', cursor_factory=RealDictCursor)
# #         cursor = conn.cursor()
# #         print("Database connection was succesfull!")
# #         break
# #     except Exception as error:
# #         print("Connecting to database failed!")
# #         print("Error: ", error)
# #         time.sleep(2)
        
# my_posts = [{"titel":"titel of post 1", "content":"content of post1", "id":1},{"titel":"favoarite foods", "content":"I like pizza","id":2}]

# def find_post(id):
#     for p in my_posts:
#         if p['id']==id:
#             return p

# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         if p['id'] == id:
#             return i

# # Define a simple endpoint
# @app.get("/")
# def read_root():
#     return {"message": "Hello, FastAPI!"}

# @app.get("/posts")
# def get_posts():
#     cursor.execute("""SELECT * FROM post""")
#     posts=cursor.fetchall()
#     return {"data":posts}
  

# @app.post("/createposts", status_code=status.HTTP_201_CREATED)
# def create_posts(post: Post):
#     # print(post.rating)
#     # print(post.dict())
#     post_dict = post.dict()
#     post_dict['id'] = randrange(0, 1000000)
#     my_posts.append(post_dict)
#     return {"data":post_dict}
#     # return {"post":f"title {payload['title']}  content {payload['content']} succesfully created posts"}

# @app.get("/posts/{id}")
# def get_posts(id: int, response:Response):
    
#     post = find_post(id)
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found")
#         # response.status_code = status.HTTP_404_NOT_FOUND
#         # return{'message':f"post with id: {id} was not found"}
#     return {"post_detail":post}

# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):
#     index = find_index_post(id)
#     if index == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} dose not exist")
#     my_posts.pop(index)
#     return Response(status_code=status.HTTP_204_NO_CONTENT)

# @app.put("/posts/{id}")
# def update_post(id: int, post: Post):
#     print(post)
#     index = find_index_post(id)
#     if index == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} dose not exist")
#     post_dict = post.dict()
#     post_dict['id'] = id
#     my_posts[index] = post_dict
#     return {'data':post_dict}
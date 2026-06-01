from fastapi import FastAPI,HTTPException,status,Query,Body,Path
from typing import Annotated
from App.schemas import newPost,postResponse
from App.db import Post,create_db_and_tables, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager

# asynccontextmanager: تُستخدم لإنشاء context manager غير متزامن
# يعني: كود يتم تنفيذه عند بدء التطبيق وإغلاقه (startup / shutdown lifecycle)
@asynccontextmanager
async def lifespan(app:FastAPI):
    await create_db_and_tables()
    yield

app= FastAPI(lifespan=lifespan)

text_posts = {
    1: {"title": "new post 1", "content": "cool test post 1"},
    2: {"title": "new post 2", "content": "cool test post 2"},
    3: {"title": "new post 3", "content": "cool test post 3"},
    4: {"title": "new post 4", "content": "cool test post 4"},
    5: {"title": "new post 5", "content": "cool test post 5"},
    6: {"title": "new post 6", "content": "cool test post 6"},
    7: {"title": "new post 7", "content": "cool test post 7"},
    8: {"title": "new post 8", "content": "cool test post 8"},
    9: {"title": "new post 9", "content": "cool test post 9"},
    10: {"title": "new post 10", "content": "cool test post 10"},
}

@app.get("/all-posts")
def getAllPosts(size:Annotated[int | None,Query()]=None):
    if size:
        return list(text_posts.values())[:size]
    return text_posts

@app.get("/post/{id}")
def getPostID(id):
    if id not in text_posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post is not exist")
    return {"post": text_posts.get(id)}

@app.post("/post/new",response_model=postResponse)
def createNewPost(newPost:Annotated[newPost,Body()]):
    new_post= {"title": newPost.title, "content": newPost.content}
    new_id=max(text_posts.keys())+ 1
    text_posts[new_id] = new_post
    return {"id": new_id, "title":new_post["title"],"content":new_post["content"]}

@app.delete("/posts/delete/${id}")
def deletePost(id:Annotated[int,Path()]):
    if id not in text_posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="id not found")
    del text_posts[id]
    return {"message": "success"}
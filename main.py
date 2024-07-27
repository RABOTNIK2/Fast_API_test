from fastapi import FastAPI
from api.handlers import user_router
from api.post_handlers import post_router

app = FastAPI(title='Social_net')

app.include_router(user_router)
app.include_router(post_router)
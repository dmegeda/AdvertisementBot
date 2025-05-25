from fastapi import FastAPI
from routers import posts
from routers import users

app = FastAPI(
    title="Ads Bot API",
    description="API for managing ads, users, comments via Telegram bot",
    version="1.0.0"
)

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(posts.router, prefix="/posts", tags=["Posts"])

@app.get("/")
def root():
    return {"message": "Welcome to Telegram Bot API"}
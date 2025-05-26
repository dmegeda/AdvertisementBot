from fastapi import FastAPI
from routers import posts, users, categories

app = FastAPI(
    title="Ads Bot API",
    description="API for managing ads, users, comments via Telegram bot",
    version="1.0.0"
)

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(posts.router, prefix="/posts", tags=["Posts"])
app.include_router(categories.router, prefix="/categories", tags=["Categories"])

@app.get("/")
def root():
    return {"message": "Welcome to Telegram Bot API"}
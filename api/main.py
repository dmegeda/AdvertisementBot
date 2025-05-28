from fastapi import FastAPI

from routers import posts
from routers import users
from routers import categories


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



if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
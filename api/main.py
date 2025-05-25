from fastapi import FastAPI
from routers import ads, users

app = FastAPI(
    title="Ads Bot API",
    description="API for managing ads, users, comments via Telegram bot",
    version="1.0.0"
)

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(ads.router, prefix="/ads", tags=["Ads"])

@app.get("/")
def root():
    return {"message": "Welcome to Ads API"}
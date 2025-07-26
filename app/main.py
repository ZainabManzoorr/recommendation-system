from fastapi import FastAPI
from app.api import recommend, bodytype, weather,avatar,skintone

app = FastAPI(title="SmartCloset Recommendation API")

@app.get("/")
def root():
    return {"message": "SmartCloset API is up and running!"}

app.include_router(recommend.router, prefix="/api")
app.include_router(bodytype.router, prefix="/api")
app.include_router(weather.router, prefix='/api')
app.include_router(avatar.router, prefix="/api")
app.include_router(skintone.router, prefix='/api')

import logging

logging.basicConfig(level=logging.DEBUG)
import mediapipe as mp
print(mp.__version__)
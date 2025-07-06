from fastapi import FastAPI
from backend_supabase.routes import predict_body_type,generate_recommendation

app = FastAPI()

app.include_router(predict_body_type.router)
app.include_router(generate_recommendation.router)
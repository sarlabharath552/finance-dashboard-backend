from fastapi import FastAPI
from app.db.database import engine, Base
from app.models import user, record
from app.api.routes import auth, users
from app.api.routes import records
from app.api.routes import dashboard



Base.metadata.create_all(bind=engine)

app = FastAPI(title="Finance Dashboard API")

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(records.router, prefix="/records", tags=["Records"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])




@app.get("/")
def home():
    return {"message": "Backend is running 🚀"}
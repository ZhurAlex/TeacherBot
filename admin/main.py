import uvicorn
from fastapi import FastAPI
from admin.routes import router as admin_router

app = FastAPI(title="TeacherBot API")
app.include_router(admin_router)

if __name__ == "__main__":
    uvicorn.run(app)
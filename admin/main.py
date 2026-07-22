import uvicorn
from fastapi import FastAPI
from admin.routes import router as admin_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="TeacherBot API")
app.include_router(admin_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app)
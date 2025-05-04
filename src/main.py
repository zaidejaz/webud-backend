from fastapi import FastAPI
from src.routes import template, chat
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.include_router(template.router, prefix="/api", tags=["templates"])
app.include_router(chat.router, prefix="/api", tags=["chat"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/health")
async def health():
    return {"status": "ok"}


from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, folders, media, ai

app = FastAPI(title="SaiuNaMídia API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include modular routers
app.include_router(auth.router)
app.include_router(folders.router)
app.include_router(media.router)
app.include_router(ai.router)


@app.get("/")
async def read_index():
    return FileResponse("template/index.html")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from audio_controller import router as audio_router
import uvicorn

app = FastAPI(title="Ava Assist")

app.include_router(audio_router)
app.mount("/", StaticFiles(directory="wwwroot", html=True), name="wwwroot")
app.mount("/audio", StaticFiles(directory="."), name="audio")

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=5000, reload=True)

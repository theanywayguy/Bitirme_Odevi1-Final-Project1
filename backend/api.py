from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from backend.routes import image_routes, video_routes, websocket_routes
from backend.core.exceptions import http_exception_handler
from fastapi import HTTPException

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(image_routes.router)
app.include_router(video_routes.router)
app.include_router(websocket_routes.router)

app.add_exception_handler(HTTPException, http_exception_handler)

@app.get("/")
async def root():
    return FileResponse("static/index.html")

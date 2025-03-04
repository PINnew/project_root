from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from datetime import datetime, timedelta
from database import init_db, get_photos_by_date
from camera_manager import start_camera, stop_camera, is_camera_running
from sse_manager import event_generator, add_event
import os


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/photos", StaticFiles(directory="photos"), name="photos")

init_db()


@app.get("/", response_class=HTMLResponse)
def get_home():
    with open("static/index.html", "r", encoding="utf-8") as file:
        return file.read()


@app.get("/start")
def start():
    if not is_camera_running():
        start_camera()
    return {"status": "Camera started"}


@app.get("/stop")
def stop():
    if is_camera_running():
        stop_camera()
    return {"status": "Camera stopped"}


@app.get("/events")
def events():
    return StreamingResponse(event_generator(), media_type="text/event-stream")


@app.get("/humans")
def get_humans(start_date: str, end_date: str):
    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    end_dt = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)
    photos = get_photos_by_date(start_dt, end_dt)
    return {"photos": [f"/photos/{photo}" for photo in photos]}

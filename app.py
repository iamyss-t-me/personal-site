from fastapi import FastAPI, Request
import uvicorn
from DB.video import DB
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import random

app = FastAPI()
db = DB()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/ss/static", StaticFiles(directory="static"), name="static")
app.mount("/v/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="template")



def random_choice(choices):
    return random.choice(choices)


@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/ss/{ss_id}")
async def read_ss(ss_id: str,request: Request):
    video = db.get_video(ss_id)
    if video is None:
        return templates.TemplateResponse("404.html", {"request": request})
    else:
        return templates.TemplateResponse("ss.html", {"request": request, "video": video})

@app.get("/v/{video_id}")
async def read_video(video_id: str,request: Request):
    video = db.get_video(video_id)
    if video is None:
        return templates.TemplateResponse("404.html", {"request": request})
    else:
        return templates.TemplateResponse("video.html", {"request": request, "video": video,"random":random_choice})



if __name__ == "__main__":
    uvicorn.run(app,debug=True)

import subprocess
import os
import urllib
import re
import unicodedata
from fastapi import FastAPI, Request, Form, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pytube import YouTube

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


def to_slug(string: str) -> str:
    string = string.strip()
    string = unicodedata.normalize('NFKD', string).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    string = string.replace('ñ', 'n')
    string = re.sub(r'\s+', '-', string)
    string = re.sub(r'[^\w-]', '', string).lower()
    return string[:40]


def get_mp3_name(title):
    return to_slug(title)


@app.post("/", response_class=HTMLResponse)
async def index_post(request: Request, url: str = Form()):
    video = YouTube(url)
    mp3_name = get_mp3_name(video.title)

    if not os.path.exists(f'static/downloads/{mp3_name}.mp3'):
        print("running job!!!")
        process = subprocess.Popen(['python', 'download.py', url, mp3_name],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.DEVNULL,
                                   )

    url_encode = urllib.parse.quote_plus(url)
    return RedirectResponse("/status?url=" + url_encode, status_code=303)


@app.get("/status", response_class=HTMLResponse)
async def status(request: Request, url: str = Query()):
    video = YouTube(url)
    mp3_name = get_mp3_name(video.title)
    title = video.title
    thumb = video.thumbnail_url
    download_url = None

    if os.path.exists(f'static/downloads/{mp3_name}.mp3'):
        download_url = f'/static/downloads/{mp3_name}.mp3'

    return templates.TemplateResponse("index_post.html", {"request": request, "title": title, 'url': url, "thumb": thumb, "download_url": download_url})

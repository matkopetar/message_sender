from fastapi import FastAPI, WebSocket, Request
from fastapi.templating import Jinja2Templates

from app.constants import TEMPLATES_DIR


app = FastAPI()

templates = Jinja2Templates(directory=TEMPLATES_DIR)


@app.get('/')
async def index(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


@app.websocket('/send_message')
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f'Message text was: {data}')



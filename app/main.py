from typing import List

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.templating import Jinja2Templates

from app.models import database, messages
from app.schemas import MessageSchema
from app.connection_manager import manager
from app.utils.constants import TEMPLATES_DIR

app = FastAPI()

templates = Jinja2Templates(directory=TEMPLATES_DIR)


@app.get('/')
async def index(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


@app.get('/messages/{client_id}', response_model=List[MessageSchema])
async def list_messages(client_id: int):
    query = messages.select().where(messages.c.client_id == client_id)
    all_messages = await database.fetch_all(query)
    return all_messages


@app.websocket('/ws/{client_id}')
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            text = await websocket.receive_text()
            query = messages.insert().values(text=text, client_id=client_id)
            await database.execute(query)

            await manager.send_personal_message(f'You wrote: {text}', websocket)
            await manager.broadcast(f'Client #{client_id} says: {text}')
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f'Client #{client_id} left the chat')


@app.on_event('startup')
async def startup():
    await database.connect()


@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()

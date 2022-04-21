from typing import List
import aioredis
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.templating import Jinja2Templates

from app.models import database
from app.schemas.message import MessageSchema
from app.services.message import MessageService
from app.services.resolver import ResolverService
from app.utils.constants import TEMPLATES_DIR, MAX_NUMBER_OF_WEBSOCKET_SERVERS

app = FastAPI()

templates = Jinja2Templates(directory=TEMPLATES_DIR)

message_service = MessageService()


@app.on_event('startup')
async def startup():
    await database.connect()


@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()


@app.get('/')
async def index(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


@app.get('/messages/{client_id}', response_model=List[MessageSchema])
async def list_messages_by_client_id(client_id: int):
    client_messages = await MessageService.get_messages_by_client_id(client_id)
    return client_messages


@app.get('/messages', response_model=List[MessageSchema])
async def list_messages():
    all_messages = await MessageService.get_all_messages()
    return all_messages


@app.get('/register')
async def register():
    new_server_registered = await ResolverService.register_new_server()
    if not new_server_registered:
        return {'message': 'Cannot register new WS server.'}

    return {'message': 'New server registered successfully'}


@app.get('/hello')
async def hello():
    server_name = await ResolverService.assign_websocket_server()
    return server_name


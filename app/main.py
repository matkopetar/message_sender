from typing import List
import aioredis
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.templating import Jinja2Templates

from app.models import database, messages
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
    query = messages.select().where(messages.c.client_id == client_id)
    all_messages = await database.fetch_all(query)
    return all_messages


@app.get('/messages', response_model=List[MessageSchema])
async def list_messages():
    query = messages.select()
    all_messages = await database.fetch_all(query)
    return all_messages


@app.get('/register')
async def register():
    redis = aioredis.from_url('redis://redis', db=1)

    ws_server_number = int(await redis.get('ws_server_number')) if await redis.get('ws_server_number') else 0
    if ws_server_number >= MAX_NUMBER_OF_WEBSOCKET_SERVERS:
        return {'message': 'Cannot register new WS server.'}

    await ResolverService.register_new_server(ws_server_number + 1)
    return {'message': 'New server registered successfully'}


@app.get('/hello')
async def hello():
    server_name = await ResolverService.assign_websocket_server()
    return server_name


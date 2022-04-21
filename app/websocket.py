from fastapi import FastAPI, WebSocket

from app.connection_manager import manager
from app.models import database
from app.redis import redis_connector_for_websocket

websocket_app = FastAPI()


@websocket_app.on_event('startup')
async def startup():
    await database.connect()


@websocket_app.on_event('shutdown')
async def shutdown():
    await database.disconnect()


@websocket_app.websocket('/{server_name}/ws/{client_id}')
async def websocket_endpoint(websocket: WebSocket, server_name: str, client_id: int):
    await manager.connect(websocket)
    await redis_connector_for_websocket(websocket, server_name, client_id)

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request

from app.models import database
from app.services.message import MessageService
from app.services.resolver import ResolverService
from app.connection_manager import manager

websocket_app = FastAPI()

message_service = MessageService()


@websocket_app.on_event('startup')
async def startup():
    await database.connect()


@websocket_app.on_event('shutdown')
async def shutdown():
    await database.disconnect()


@websocket_app.websocket('/{server_name}/ws/{client_id}')
async def websocket_endpoint(websocket: WebSocket, server_name: str, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            text = await websocket.receive_text()
            output_text = await message_service.insert_message_and_get_output_text(text=text, client_id=client_id)

            await manager.send_personal_message(f'Received message: {output_text}', websocket)
            await manager.broadcast(f'Client #{client_id} says: {output_text}')
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await ResolverService.lower_connection_number(server_name)

        await manager.broadcast(f'Client #{client_id} left the chat')


import os
import asyncio
import aioredis
import async_timeout
from fastapi import WebSocket, WebSocketDisconnect

from app.services.message import MessageService
from app.services.resolver import ResolverService
from app.connection_manager import manager


async def websocket_handler(ws: WebSocket, server_name: str, client_id: int, r):
    try:
        while True:
            text = await ws.receive_text()
            output_text = await MessageService.insert_message_and_get_output_text(text=text, client_id=client_id)
            await manager.send_personal_message(f'You sent: {output_text}', ws)
            await r.publish(os.environ.get('REDIS_CHANNEL'), f'Client #{client_id} says: {output_text}')
    except WebSocketDisconnect:
        manager.disconnect(ws)
        await ResolverService.lower_connection_number(server_name)

        await r.publish(os.environ.get('REDIS_CHANNEL'), f'Client #{client_id} left the chat')


async def reader(channel: aioredis.client.PubSub, ws: WebSocket):
    while True:
        try:
            async with async_timeout.timeout(1):
                message = await channel.get_message(ignore_subscribe_messages=True)
                if message is not None:
                    await manager.send_personal_message(message.get('data').decode('utf-8'), ws)
                await asyncio.sleep(0.01)
        except asyncio.TimeoutError:
            pass


async def redis_subscriber(r, websocket):
    pubsub = r.pubsub()
    await pubsub.subscribe(os.environ.get('REDIS_CHANNEL'))

    await asyncio.create_task(reader(pubsub, websocket))


async def redis_connector_for_websocket(websocket: WebSocket, server_name: str, client_id: int):
    redis = aioredis.from_url(os.environ.get('REDIS_URL'))

    publisher_task = websocket_handler(websocket, server_name, client_id, redis)
    subscriber_task = redis_subscriber(redis, websocket)
    done, pending = await asyncio.wait(
        [publisher_task, subscriber_task], return_when=asyncio.FIRST_COMPLETED,
    )

    for task in pending:
        task.cancel()

import aioredis
import os
from typing import Union

from app.utils.constants import WEBSOCKET_SERVER_PREFIX, MAX_NUMBER_OF_WEBSOCKET_SERVERS


class ResolverService:

    @staticmethod
    async def _register_new_server() -> int:
        redis = aioredis.from_url(os.environ.get('REDIS_URL'))

        ws_server_number = int(await redis.get('ws_server_number')) if await redis.get('ws_server_number') else 0
        if ws_server_number >= MAX_NUMBER_OF_WEBSOCKET_SERVERS:
            return -1

        return ws_server_number + 1

    @classmethod
    async def register_new_server(cls) -> bool:
        server_to_register = await cls._register_new_server()
        if server_to_register <= 0:
            return False

        redis = aioredis.from_url(os.environ.get('REDIS_URL'))
        await redis.set('ws_server_number', server_to_register)

        server_name = WEBSOCKET_SERVER_PREFIX + str(server_to_register)
        await redis.set(server_name + '_connection_number', 0)

        return True

    @staticmethod
    async def assign_websocket_server() -> Union[None, str]:
        redis = aioredis.from_url(os.environ.get('REDIS_URL'))

        number_of_servers = int(await redis.get('ws_server_number')) if await redis.get('ws_server_number') else 0

        if number_of_servers:
            server_one = WEBSOCKET_SERVER_PREFIX + '1'
            assigned_server = server_one

            min_number_of_connections = int(await redis.get(server_one + '_connection_number'))
            for server in range(2, number_of_servers + 1):
                server_name = WEBSOCKET_SERVER_PREFIX + str(server)
                number_of_connections = int(await redis.get(server_name + '_connection_number'))
                if number_of_connections < min_number_of_connections:
                    min_number_of_connections = number_of_connections
                    assigned_server = server_name

            await redis.set(assigned_server + '_connection_number', min_number_of_connections + 1)
            return assigned_server

        return ''

    @staticmethod
    async def lower_connection_number(server_name):
        redis = aioredis.from_url(os.environ.get('REDIS_URL'))

        connection_number = int(await redis.get(server_name + '_connection_number'))
        await redis.set(server_name + '_connection_number', connection_number - 1)

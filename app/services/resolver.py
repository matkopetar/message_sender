import aioredis
from typing import Union

from app.utils.constants import WEBSOCKET_SERVER_PREFIX


class ResolverService:

    @staticmethod
    async def register_new_server(server_to_register: int) -> None:
        redis = aioredis.from_url('redis://redis', db=1)

        await redis.set('ws_server_number', server_to_register)

        server_name = WEBSOCKET_SERVER_PREFIX + str(server_to_register)
        await redis.set(server_name + '_connection_number', 0)

    @staticmethod
    async def assign_websocket_server() -> Union[None, str]:
        redis = aioredis.from_url('redis://redis', db=1)

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
        redis = aioredis.from_url('redis://redis', db=1)

        connection_number = int(await redis.get(server_name + '_connection_number'))
        await redis.set(server_name + '_connection_number', connection_number - 1)

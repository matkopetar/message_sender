import aioredis


class ResolverService:

    @staticmethod
    async def register_new_server(server_to_register: int) -> None:
        redis = aioredis.from_url('redis://redis', db=1)

        await redis.set('ws_server_number', server_to_register)

    @staticmethod
    async def assign_websocket_server() -> None:
        pass

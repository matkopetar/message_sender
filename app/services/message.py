from typing import List

from app.models import database, messages
from app.schemas.message import MessageSchema
from app.utils.modifiers import modify_message_text, INPUT_MODIFIER, OUTPUT_MODIFIER


class MessageService:
    @staticmethod
    async def insert_message_and_get_output_text(text: str, client_id: int) -> str:
        modified_input_text = modify_message_text(text, INPUT_MODIFIER)
        query = messages.insert().values(text=modified_input_text, client_id=client_id)
        await database.execute(query)

        modified_output_text = modify_message_text(modified_input_text, OUTPUT_MODIFIER)

        return modified_output_text

    @staticmethod
    async def get_all_messages() -> List[MessageSchema]:
        query = messages.select()
        all_messages = await database.fetch_all(query)

        return all_messages

    @staticmethod
    async def get_messages_by_client_id(client_id: int) -> List[MessageSchema]:
        query = messages.select().where(messages.c.client_id == client_id)
        all_messages = await database.fetch_all(query)

        return all_messages

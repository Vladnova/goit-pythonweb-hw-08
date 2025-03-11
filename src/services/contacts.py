from sqlalchemy.ext.asyncio import AsyncSession


from src.repository.contacts import ContactRepository
from src.schemas import ContactBase, ContactUpdate


class ContactService:
    def __init__(self, db: AsyncSession):
        self.repository = ContactRepository(db)

    async def create_contact(self, contact: ContactBase):
        return await self.repository.create_contact(contact)

    async def get_contacts(self, skip: int, limit: int):
        return await self.repository.get_contacts(skip, limit)

    async def get_contact(self, contact_id: int):
        return await self.repository.get_contact_by_id(contact_id)

    async def update_contact(self, contact_id: int, body: ContactUpdate ):
        return await self.repository.update_contact(contact_id, body)

    async def delete_contact(self, contact_id: int):
        return await self.repository.delete_contact(contact_id)

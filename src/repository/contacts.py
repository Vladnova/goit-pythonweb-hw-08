from typing import List

from sqlalchemy import select

from sqlalchemy.ext.asyncio import  AsyncSession

from src.database.models import Contact
from src.schemas import ContactBase, ContactUpdate

class ContactRepository:
    def __init__(self, session: AsyncSession):
        self.db = session
    async def get_contacts(self, skip: int, limit: int) -> List[Contact]:
        stmt = select(Contact).offset(skip).limit(limit)
        contacts = await self.db.execute(stmt)
        return list(contacts.scalars().all())

    async def get_contact_by_id(self, contact_id: int) -> Contact | None:
        stmt = select(Contact).where(Contact.id == contact_id)
        contact = await self.db.execute(stmt)
        return contact.scalar_one_or_none()

    async def create_contact(self, contact: ContactBase) -> Contact:
        new_contact = Contact(**contact.model_dump(exclude_unset=True))
        self.db.add(new_contact)
        await self.db.commit()
        await self.db.refresh(new_contact)
        return new_contact

    async def update_contact(self, contact_id: int, body: ContactUpdate ) -> Contact | None:

        contact = await self.get_contact_by_id(contact_id)
        if contact:
            contact.name = body.name
            contact.last_name = body.last_name
            contact.email = body.email
            contact.phone = body.phone
            await self.db.commit()
            await self.db.refresh(contact)
        return contact

    async def delete_contact(self, contact_id: int) -> Contact:
        contact = await self.get_contact_by_id(contact_id)
        if contact:
            await self.db.delete(contact)
            await self.db.commit()
        return contact


__all__ = ('AdminRepository')

from app.models import Admin


class AdminRepository:
    def __init__(self):
        self.collection = Admin

    async def add_admin(self, new_admin: Admin) -> Admin:
        admin = await new_admin.create()
        return admin

    async def get_admin(self, email: str) -> Admin:
        return await self.collection.find_one(Admin.email == email)

from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from passlib.context import CryptContext

from app.repositories.admin import AdminRepository

security = HTTPBasic()
hash_helper = CryptContext(schemes=["bcrypt"])


async def validate_login(
        credentials: HTTPBasicCredentials = Depends(security),
        admin_repo: AdminRepository = Depends(AdminRepository)
):
    admin = await admin_repo.get_admin(credentials.username)
    if admin:
        password = hash_helper.verify(credentials.password, admin["password"])
        if not password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
            )
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password"
    )

from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from passlib.context import CryptContext

from app.repositories.admin import AdminRepository

security = HTTPBasic()
hash_helper = CryptContext(schemes=["bcrypt"])


async def validate_login(
    credentials: HTTPBasicCredentials = Depends(security),
    admin_repo: AdminRepository = Depends(AdminRepository)
) -> bool:
    """
    Validate admin login credentials.
    Raises HTTPException with 401 status if credentials are invalid.
    """
    try:
        admin = await admin_repo.get_admin(credentials.username)
        if not admin or not hash_helper.verify(credentials.password, admin["password"]):
            # Use constant-time comparison to prevent timing attacks
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
            )
        return True
    except Exception as e:
        # Log the error here if you have logging set up
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
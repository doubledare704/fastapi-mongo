from fastapi import Body, APIRouter, HTTPException, Depends
from passlib.context import CryptContext

from app.auth.jwt_handler import sign_jwt
from app.models import Admin
from app.repositories import AdminRepository
from app.schemas.admin import AdminData, AdminSignIn

router = APIRouter()

hash_helper = CryptContext(schemes=["bcrypt"])


@router.post("/login")
async def admin_login(admin_credentials: AdminSignIn = Body(...), ar: AdminRepository = Depends(AdminRepository)):
    admin_exists = await ar.get_admin(email=admin_credentials.username)
    if admin_exists:
        password = hash_helper.verify(admin_credentials.password, admin_exists.password)
        if password:
            return sign_jwt(admin_credentials.username)

        raise HTTPException(status_code=403, detail="Incorrect email or password")

    raise HTTPException(status_code=403, detail="Incorrect email or password")


@router.post("/signup", response_model=AdminData)
async def admin_signup(admin: Admin = Body(...), ar: AdminRepository = Depends(AdminRepository)):
    admin_exists = await ar.get_admin(email=admin.email)
    if admin_exists:
        raise HTTPException(
            status_code=409, detail="Admin with email supplied already exists"
        )

    admin.password = hash_helper.encrypt(admin.password)
    new_admin = await ar.add_admin(new_admin=admin)
    return new_admin

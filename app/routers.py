from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from .models import OrgCreate, OrgUpdate, OrgDelete, OrganizationOut, Token
from .services import OrgService, AdminService
from .auth import create_access_token, get_current_admin
from .config import settings

router = APIRouter()

@router.post("/org/create", response_model=OrganizationOut)
async def create_organization(payload: OrgCreate):
    return await OrgService.create_org(payload.organization_name, payload.email, payload.password)

@router.get("/org/get", response_model=OrganizationOut)
async def get_organization(organization_name: str):
    return await OrgService.get_org_by_name(organization_name)

@router.put("/org/update")
async def update_organization(payload: OrgUpdate, token_data: dict = Depends(get_current_admin)):
    return await OrgService.update_org(
        current_name=payload.current_name,
        new_name=payload.new_name,
        email=payload.email,
        password=payload.password,
        requesting_org_id=token_data["org_id"]
    )

@router.delete("/org/delete")
async def delete_organization(payload: OrgDelete, token_data: dict = Depends(get_current_admin)):
    return await OrgService.delete_org(payload.organization_name, requesting_org_id=token_data["org_id"])

@router.post("/admin/login", response_model=Token)
async def admin_login(form_data: OAuth2PasswordRequestForm = Depends()):
    email = form_data.username
    password = form_data.password
    auth = await AdminService.authenticate(email, password)
    if not auth:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    admin, org = auth
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"admin_id": str(admin["_id"]), "org_id": str(org["_id"])},
        expires_delta=access_token_expires
    )
    return Token(access_token=access_token)

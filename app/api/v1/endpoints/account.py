import base64

from authx import TokenPayload
from fastapi import APIRouter, Depends, Form, UploadFile, File
from starlette.responses import JSONResponse

from app.core import get_account_service, security, config, get_current_user_safe, get_avatar_service
from app.schemas import AccountSchema, RoleIdSchema, LoginSchema
from app.services import AccountService, AvatarService

account_router = APIRouter(tags=['Accounts'], prefix='/accounts')

@account_router.post('/login', response_class=JSONResponse)
async def login(account: LoginSchema, service: AccountService = Depends(get_account_service)):
    hash = await service.get_password_hash_by_login(account.login)
    if hash is None:
        return JSONResponse('Wrong credentials', status_code=404)

    user_id = await service.login(account, hash)
    token = security.create_access_token(str(user_id))
    response = JSONResponse('Success')
    response.set_cookie(
        config.JWT_ACCESS_COOKIE_NAME,
        token,
        httponly=True,
        samesite='lax',
        secure=False,
        path='/',
        max_age=3600
    )
    return response

@account_router.get('/logout', response_class=JSONResponse)
async def logout():
    response = JSONResponse('Success')
    response.delete_cookie(config.JWT_ACCESS_COOKIE_NAME)
    return response

@account_router.post('/register', response_class=JSONResponse)
async def register(
        login: str = Form(...),
        password: str = Form(...),
        name: str = Form(...),
        surname: str = Form(...),
        patronymic: str | None = Form(None),
        phone_number: str | None = Form(None),
        email: str | None = Form(None),
        short_description: str = Form(...),
        avatar: UploadFile = File(...),
        avatar_service: AvatarService = Depends(get_avatar_service),
        account_service: AccountService = Depends(get_account_service)):

    file_bytes = await avatar.read()
    avatar_id = await avatar_service.add_avatar(file_bytes)
    if avatar_id is None:
        return

    account_schema = AccountSchema(
        login = login,
        password = password,
        name = name,
        surname = surname,
        patronymic = patronymic,
        short_description = short_description,
        phone_number = phone_number,
        email = email,
        avatar_id = avatar_id,
        role_id=2
    )
    user_id = await account_service.register(account_schema)
    if user_id is None:
        await avatar_service.delete_avatar(avatar_id)
        return JSONResponse('Wrong credentials', status_code=404)

    token = security.create_access_token(str(user_id))
    response = JSONResponse('Success')
    response.set_cookie(
        config.JWT_ACCESS_COOKIE_NAME,
        token,
        httponly=True,
        samesite='lax',
        secure=False,
        path='/',
        max_age=3600
    )
    return response

@account_router.get('/me')
async def get_user_id(current_user: TokenPayload = Depends(get_current_user_safe)) -> int:
    user_id = int(current_user.sub)
    return user_id

@account_router.get('/me/login')
async def get_user_login(service: AccountService = Depends(get_account_service), current_user=Depends(get_current_user_safe)):
    user_id = int(current_user.sub)
    user_login = await service.get_user_login(user_id)
    return user_login

@account_router.get('/auth-data')
async def get_user_data(service: AccountService = Depends(get_account_service), avatar_service: AvatarService = Depends(get_avatar_service), current_user=Depends(get_current_user_safe)):
    if current_user.sub == 'None':
        return JSONResponse('Wrong data', status_code=404)
    user_id = int(current_user.sub)
    user_data = await service.get_user_data_for_profile(user_id)
    user_login = user_data.login
    name = f'{user_data.name} {user_data.surname} {user_data.patronymic}'
    role_id = user_data.role_id
    role_name = await service.get_role_name_by_role_id(role_id)
    avatar = await avatar_service.get_avatar_by_user_id(user_id)
    avatar_b64 = base64.b64encode(avatar).decode('utf-8') if avatar else None
    return user_id, user_login, name, avatar_b64, role_id, role_name

@account_router.get('/get-user-data-for-profile')
async def get_user_data_for_profile(service: AccountService = Depends(get_account_service), avatar_service: AvatarService = Depends(get_avatar_service), current_user=Depends(get_current_user_safe)):
    user_id = int(current_user.sub)
    user_data = await service.get_user_data_for_profile(user_id)
    avatar = await avatar_service.get_avatar_by_user_id(user_id)
    avatar_b64 = base64.b64encode(avatar).decode('utf-8') if avatar else None
    user_data.avatar = avatar_b64
    return user_data

@account_router.post('/get-role-name')
async def get_role_name(role: RoleIdSchema, service: AccountService = Depends(get_account_service)):
    res = await service.get_role_name_by_role_id(role.role_id)
    return res

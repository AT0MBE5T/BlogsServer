from app.core import Hashing
from app.interfaces import IAccountService, IAccountRepository
from app.models import Account
from app.schemas import AccountSchema, LoginSchema, UserProfileSchema


class AccountService(IAccountService):

    def __init__(self, repository: IAccountRepository):
        self._repository = repository

    async def get_user_id(self, account: AccountSchema) -> int | None:
        user_id = await self._repository.get_user_id(account.login)
        return user_id

    async def get_user_login(self, id: int) -> str | None:
        user_id = await self._repository.get_user_login(id)
        return user_id

    async def get_password_hash_by_login(self, login: str):
        return await self._repository.get_password_hash_by_login(login)

    async def register(self, account_data: AccountSchema) -> str | None:
        hashed_password = Hashing.hash_bcrypt(account_data.password)
        new_account = Account(
            login=account_data.login,
            password=hashed_password,
            name=account_data.name,
            surname=account_data.surname,
            patronymic=account_data.patronymic,
            short_description=account_data.short_description,
            phone_number=account_data.phone_number,
            email=account_data.email,
            avatar_id=account_data.avatar_id,
            role_id=account_data.role_id
        )
        user_id = await self._repository.register(new_account)
        return str(user_id) if user_id else None

    async def login(self, login_data: LoginSchema, hash: str) -> str | None:
        isCorrect = Hashing.check_bcrypt(login_data.password, hash)
        if isCorrect:
            return await self._repository.get_user_id(login_data.login)
        return None

    async def get_name_by_user_id(self, user_id: int) -> str | None:
        (name, surname) = await self._repository.get_name_by_user_id(user_id)
        return f'{name} {surname}'

    async def get_user_data_for_full_blog_info(self, user_id: int):
        res = await self._repository.get_data_for_blog(user_id)
        return res

    async def get_role_name_by_role_id(self, role_id: int) -> str:
        res = await self._repository.get_role_name_by_role_id(role_id)
        return res

    async def get_user_data_for_profile(self, user_id: int) -> UserProfileSchema:
        res = await self._repository.get_data_for_profile(user_id)
        role_name = await self.get_role_name_by_role_id(res.role_id)
        user_profile = UserProfileSchema(
            login=res.login,
            name=res.name,
            surname=res.surname,
            patronymic=res.patronymic,
            short_description=res.short_description,
            phone_number=res.phone_number,
            email=res.email,
            avatar=bytes(),
            role_id=res.role_id,
            role_name=role_name
        )

        return user_profile



from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext

from app.config import get_auth_data
from app.users.dao import UsersDAO


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


def get_password_hash(password: str) -> str:
    """
    Принимает обычный пароль и возвращает его хеш.
    В базу данных сохраняем только хеш, а не исходный пароль.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Сравнивает обычный пароль с хешем из базы данных.
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    """
    Создаёт JWT-токен.
    В токен кладём данные пользователя и срок действия токена.
    """
    auth_data = get_auth_data()

    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(days=7)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        auth_data["secret_key"],
        algorithm=auth_data["algorithm"],
    )

    return encoded_jwt


async def authenticate_user(email: str, password: str):
    """
    Проверяет пользователя по email и паролю.
    Если пользователь найден и пароль верный — возвращает пользователя.
    Если нет — возвращает None.
    """
    user = await UsersDAO.find_one_or_none(email=email)

    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user
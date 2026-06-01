from fastapi import Depends, HTTPException, Request, status
from jose import JWTError, jwt

from app.config import get_auth_data
from app.users.dao import UsersDAO


def get_token(request: Request) -> str:
    """
    Достаёт JWT-токен из cookie.
    """
    token = request.cookies.get("users_access_token")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Токен отсутствует",
        )

    return token


async def get_current_user(token: str = Depends(get_token)):
    """
    Проверяет JWT-токен, достаёт из него id пользователя
    и ищет этого пользователя в базе данных.
    """
    auth_data = get_auth_data()

    try:
        payload = jwt.decode(
            token,
            auth_data["secret_key"],
            algorithms=[auth_data["algorithm"]],
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Некорректный токен",
            )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Некорректный токен",
        )

    user = await UsersDAO.find_one_or_none_by_id(int(user_id))

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не найден",
        )

    return user


async def get_current_admin_user(current_user=Depends(get_current_user)):
    """
    Проверяет, что текущий пользователь является админом.
    """
    if not current_user.is_admin and not current_user.is_super_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав",
        )

    return current_user
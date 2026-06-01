from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.users.auth import authenticate_user, create_access_token, get_password_hash
from app.users.dao import UsersDAO
from app.users.schemas import UserLogin, UserRead, UserRegister
from app.users.dependencies import get_current_user


router = APIRouter(
    prefix="/auth",
    tags=["Авторизация"],
)


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserRegister):
    existing_user_by_email = await UsersDAO.find_one_or_none(email=user_data.email)

    if existing_user_by_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь с таким email уже существует",
        )

    existing_user_by_phone = await UsersDAO.find_one_or_none(
        phone_number=user_data.phone_number
    )

    if existing_user_by_phone:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь с таким номером телефона уже существует",
        )

    user_dict = user_data.model_dump()

    hashed_password = get_password_hash(user_dict.pop("password"))

    user = await UsersDAO.add(
        **user_dict,
        hashed_password=hashed_password,
    )

    return user


@router.post("/login")
async def login_user(response: Response, user_data: UserLogin):
    user = await authenticate_user(
        email=user_data.email,
        password=user_data.password,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль",
        )

    access_token = create_access_token(
        data={"sub": str(user.id)}
    )

    response.set_cookie(
        key="users_access_token",
        value=access_token,
        httponly=True,
    )

    return {
        "message": "Пользователь успешно авторизован",
        "access_token": access_token,
    }


@router.get("/me", response_model=UserRead)
async def get_me(current_user=Depends(get_current_user)):
    return current_user


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie(key="users_access_token")

    return {
        "message": "Пользователь успешно вышел из системы",
    }

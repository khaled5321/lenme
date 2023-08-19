from .models import User


def user_create(*, data: dict) -> User:
    user = User(
        email=data["email"],
        account_type=data["account_type"],
    )

    user.set_password(data["password"])
    user.save()

    return user

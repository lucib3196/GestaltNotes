from src.model.user import UserCreate, VALID_ROLES


ROLES: list[VALID_ROLES] = ["admin","educator","student"]


USERS: list[UserCreate] = [
    UserCreate(
        first_name="Ada",
        last_name="Lovelace",
        username="ada",
        email="ada@example.com",
        password="password-1",
    ),
    UserCreate(
        first_name="Grace",
        last_name="Hopper",
        username="grace",
        email="grace@example.com",
        password="password-2",
    ),
    UserCreate(
        first_name="Katherine",
        last_name="Johnson",
        username="katherine",
        email="katherine@example.com",
        password="password-3",
    ),
]

from passlib.context import CryptContext


class PasswordHandler:
    pwd_context = CryptContext(
        schemes=["bcrypt"],
        deprecated="auto",
    )

    @staticmethod
    def generate_password_hash(password: str) -> str:
        return PasswordHandler.pwd_context.hash(password)

    @staticmethod
    def check_password_hash(hashed_password: str, plain_password: str) -> bool:
        return PasswordHandler.pwd_context.verify(plain_password, hashed_password)


password_handler: PasswordHandler = PasswordHandler()

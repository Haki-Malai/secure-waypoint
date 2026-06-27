import bcrypt


class PasswordHandler:
    def generate_password_hash(self, password: str) -> str:
        password_bytes = password.encode("utf-8")
        if len(password_bytes) > 72:
            raise ValueError("Password cannot be longer than 72 bytes")

        return bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode("utf-8")

    def check_password_hash(self, hashed_password: str, plain_password: str) -> bool:
        plain_password_bytes = plain_password.encode("utf-8")
        if len(plain_password_bytes) > 72:
            return False

        try:
            return bcrypt.checkpw(plain_password_bytes, hashed_password.encode("utf-8"))
        except ValueError:
            return False


password_handler: PasswordHandler = PasswordHandler()

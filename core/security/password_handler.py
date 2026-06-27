import bcrypt


class PasswordHandler:
    def generate_password_hash(self, password: str) -> str:
        """Generate a bcrypt hash for a plaintext password.

        :param password: The plaintext password to hash.

        :raises ValueError: If the UTF-8 encoded password exceeds bcrypt's
            72-byte input limit.

        :return: The generated bcrypt hash.
        """
        password_bytes = password.encode("utf-8")
        if len(password_bytes) > 72:
            raise ValueError("Password cannot be longer than 72 bytes")

        return bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode("utf-8")

    def check_password_hash(self, hashed_password: str, plain_password: str) -> bool:
        """Check whether a plaintext password matches a bcrypt hash.

        Invalid hashes and passwords that exceed bcrypt's byte limit are treated
        as non-matches instead of raising to callers.

        :param hashed_password: The stored bcrypt hash.
        :param plain_password: The plaintext password to verify.

        :return: True when the password matches the hash, otherwise False.
        """
        plain_password_bytes = plain_password.encode("utf-8")
        if len(plain_password_bytes) > 72:
            return False

        try:
            return bcrypt.checkpw(plain_password_bytes, hashed_password.encode("utf-8"))
        except ValueError:
            return False


password_handler: PasswordHandler = PasswordHandler()

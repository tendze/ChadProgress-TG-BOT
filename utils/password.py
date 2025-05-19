import secrets
import string

def generate_password(length: int = 12) -> str:
    if length < 4:
        raise ValueError("Пароль должен быть минимум из 4 символов")

    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for _ in range(length))

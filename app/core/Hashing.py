import bcrypt

def hash_bcrypt(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt).decode()
    return hashed

def check_bcrypt(password: str, hash: str) -> bool:
    return bcrypt.checkpw(password.encode(), hash.encode())

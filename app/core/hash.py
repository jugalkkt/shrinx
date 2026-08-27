import bcrypt

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    bin_pw = password.encode("utf-8")
    result = bcrypt.hashpw(bin_pw, salt)
    return result.decode("utf-8")

def verify_password(password: str, hashed: str) -> bool:
    password = password.encode("utf-8")
    hashed = hashed.encode("utf-8")
    return bcrypt.checkpw(password,hashed)
        
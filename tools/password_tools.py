from werkzeug.security import check_password_hash, generate_password_hash


def hash_password(password: str):
    hash_value = generate_password_hash(password)
    return hash_value


def validate_password_on_login(password: str, hash_value: str):
    if check_password_hash(hash_value, password):
        return True
    return False


def validate_password_on_register(password: str, retyped_password: str):
    if password == retyped_password:
        hash_value = hash_password(password)
        return hash_value
    return None


def validate_passwords_on_change(
    password: str,
    current_hash: str,
    new_password: str,
    retyped_new_password: str):
    if check_password_hash(current_hash, password)\
        and new_password == retyped_new_password:
        hash_value = hash_password(new_password)
        return hash_value
    return None

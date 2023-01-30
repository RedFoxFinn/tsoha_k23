from werkzeug.security import check_password_hash, generate_password_hash

def hash_password(password:str):
    hash = generate_password_hash(password)
    return hash

def validate_password_on_login(password:str, hash:str):
    if check_password_hash(hash, password):
        return True
    else:
        return False

def validate_password_on_register(password:str, retyped_password:str):
    if password == retyped_password:
        hash = hash_password(password)
        return hash
    else:
        return None

def validate_passwords_on_change(password:str, current_hash:str, new_password:str, retyped_new_password:str):
    if check_password_hash(current_hash, password) and new_password == retyped_new_password:
        hash = hash_password(new_password)
        return hash
    else:
        return None
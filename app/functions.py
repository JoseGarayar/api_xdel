from app import bcrypt


def hash_password(password):
    """
    Hashes a plain text password using bcrypt.
    
    Args:
        password (str): The plain text password to hash.

    Returns:
        str: The hashed password, decoded from bytes to a UTF-8 string.
    """
    return bcrypt.generate_password_hash(password).decode('utf-8')


def check_valid_password(db_user_password, data_password):
    """
    Checks if a provided plain text password matches the hashed password stored in the database.
    
    Args:
        db_user_password (str): The hashed password stored in the database.
        data_password (str): The plain text password to verify.

    Returns:
        bool: True if the passwords match, False otherwise.
    """
    return bcrypt.check_password_hash(db_user_password, data_password)
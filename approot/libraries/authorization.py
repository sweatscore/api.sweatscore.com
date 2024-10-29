""" Authorization library functions """

import bcrypt
import string
import random

from datetime import datetime, timedelta

from cryptography.fernet import Fernet

import library as applib

def hash_password(unhashed_password):
    """ Takes a plain text password and returns a hashed version of it """

    salt = bcrypt.gensalt()

    hashed_password = bcrypt.hashpw(unhashed_password.encode('utf-8'), salt)

    return str(hashed_password, 'utf-8')

def check_password(login_password: str, database_password: str) -> bool:
    """ Verifies that two passwords match """

    password_1 = login_password.encode('utf-8')
    password_2 = database_password.encode('utf-8')

    return bcrypt.checkpw(password_1, password_2)

def get_email_code():
    """ Generates a code to send to a user's email address """

    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

    return code

def create_session_token(
        user_id,
        session_duration = applib.DEFAULT_SESSION_DURATION,
        session_start = None,
        secret_key = applib.SWEATSCORE_SECRET_KEY):
    """ Creates a session, returning the token and expiration timestamp.  """

    # Set the default value for session_start
    if session_start is None:
        session_start = datetime.now()

    # Set the expiration time
    expiration_time = session_start + timedelta(minutes=session_duration)

    expiration_timestamp = expiration_time.timestamp()

    # Encrypt the values
    value_to_encrypt = f"{user_id}|{expiration_timestamp}"

    fernet = Fernet(bytes(secret_key, encoding='utf-8'))

    encrypted_value = fernet.encrypt(bytes(value_to_encrypt, 'utf-8'))

    # Create a JavaScript compatible time delta. This assumes
    # the client application knows its own timezone.
    expiration_timestamp = timedelta(minutes=session_duration).seconds
    javascript_timedelta = int(expiration_timestamp) * 1000

    return {
        'token': str(encrypted_value, 'utf-8'),
        'expiration': javascript_timedelta
    }

# def verify_session(
#     encrypted_value,
#     session_time = None,
#     secret_key = applib.SWEATSCORE_SECRET_KEY) -> int:
#     """ Decrypts the session token and verifies it is not expired """

#     # Set the default session time
#     if session_time is None:
#         session_time = datetime.now()

#     # Decrypt the token
#     fernet = Fernet(bytes(secret_key, encoding='utf-8'))

#     encrypted_value = fernet.encrypt(bytes(value_to_encrypt, 'utf-8'))

""" Authorization library functions """

import bcrypt

def hash_password(unhashed_password):
    """ Takes a plain text password and returns a hashed version of it """

    salt = bcrypt.gensalt()

    hashed_password = bcrypt.hashpw(unhashed_password.encode('utf-8'), salt)

    return str(hashed_password, 'utf-8')

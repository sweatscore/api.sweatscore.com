"""
    The signup library. Implements user sign-up and account verification functionality.
"""

import re

from datetime import datetime, timedelta

from sqlalchemy import select

import library as applib

from database import SweatscoreUser, EmailCode

import libraries.authorization as authlib


def new_user(request, dbsession):
    """
        Accepts the email and password from a request to create a new user account.
        Creates a new record in the users table if non exists.
        Returns an appropriate status code redirecting the user if the account needs to
        be verified or if the user is already verified.
    """

    # Check to see if a record already exists in the users table
    select_query = (
        select(SweatscoreUser)
            .where(SweatscoreUser.email_address == request.email)
    )

    user = dbsession.scalar(select_query)

    if user is None:
        # Check the password
        if not validate_password(request.password):
            return {
                'code': 'af7hj433',
                'message': "The chosen password does not meet requirements."
            }

        # Hash the password if it passes the test
        password = authlib.hash_password(request.password)

        # Create the user
        user = SweatscoreUser(
            email_address = request.email,
            password = password,
            created_at = datetime.now(),
            status_id = 1)

        # Add the user and flush the session to get the new user ID
        dbsession.add(user)

        dbsession.flush()

        # Generate a sign-up session token
        session_token = authlib.create_session_token(
            user.id,
            applib.SIGNUP_SESSION_DURATION)

        # Add the token to the user record
        user.session_token = session_token['token']

        dbsession.commit()

        # Create and store the email verification code
        # email_verification_code = get_email_code()

        # email_code = EmailCode(
        #     user_id = user.id,
        #     code = email_verification_code,
        #     created_at = datetime.now()
        # )

        # dbsession.add(email_code)

        # dbsession.commit()

        response = {
            'code': 'i8jhe643',
            'message': 'The user account has been created.',
            'session_token': session_token
        }
    # User email address needs to be verified
    elif user.status_id == 1:
        response = {
            'code': '84ei1fdf',
            'message': "User email address needs to be verified."
        }
    # The user is already signed-up. Redirect to login.
    else:
        response = {
            'code': '6216ga03',
            'message': 'The user is already signed-up.'
        }

    return response


def verify_email_address(request, dbsession):
    """
        Accepts a code that was sent to a new users email address from the request and
        verifies it against the code stored in the database.    
    """

    # Query for the code
    select_query = (
        select(EmailCode)
            .where(EmailCode.code == request.code.upper())
    )

    code = dbsession.scalar(select_query)

    if code:
        if code.created_at + timedelta(hours=2) < datetime.now():
            dbsession.delete(code)

            dbsession.commit()

            return {
                'code': 'j55j862j',
                'message': "The verification code does not exist or is expired."
            }
        else:
            code.user.status_id = 2

            dbsession.flush()

            dbsession.delete(code)

            dbsession.commit()

            return {
                'code': '86ijj0i2',
                'message': "The users email account is verified."
            }
    else:
        return {
            'code': 'j55j862j',
            'message': "The verification code does not exist or is expired."
        }


def validate_password(password):
    """
        Validates the password. It should be a certain length
        and contain the correct combination of characters.
    """

    regExp = re.compile(r'(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,50}$')

    match = re.match(regExp, password)

    if match:
        return True
    else:
        return False

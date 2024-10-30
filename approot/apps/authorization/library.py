"""
    The authorization library. Implements user log-in and security functionality.
"""

from sqlalchemy import select

from database import SweatscoreUser

import library as applib

import libraries.authorization as authlib


def login(request, dbsession):
    """
        Logs a user into Sweatscore, and returns a status code
        to indicate the success or failure of the operation.
    """

    # Look for the email address in the users table
    select_query = (
        select(SweatscoreUser)
            .where(SweatscoreUser.email_address == request.email.strip()))

    user = dbsession.scalar(select_query)

    if user:
        # Check that the password matches
        if authlib.check_password(request.password, user.password):
            # Normal condition...the user is fully signed up
            if user.status_id == 2:
                pass
            elif user.status_id == 1:
                # The user needs to complete the sign-up process
                # Generate a sign-up session token
                session_token = authlib.create_session_token(
                    user.id,
                    applib.SIGNUP_SESSION_DURATION)
        
                # Add the token to the user record
                user.session_token = session_token['token']

                dbsession.commit()

                return {
                    'code': 'i8jhe643',
                    'message': "The user account has been created.",
                    'session_token': session_token
                }
        else:
            # An incorrect password was entered
            return {
                'code': 'cfdga695',
                'message': "The password is incorrect."
            }
    else:
        return {
            'code': 'i2ddb836',
            'message': "The user does not exist."
        }
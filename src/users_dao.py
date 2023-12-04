"""
DAO (Data Access Object) file

Helper file containing functions for accessing data in our database
"""

from db import db, User


def get_user_by_email(email):
    """
    Returns a user object from the database given an email
    """
    return User.query.filter(User.email == email).first()


def get_user_by_session_token(session_token):
    """
    Returns a user object from the database given a session token
    """
    return User.query.filter(User.session_token == session_token).first()


def get_user_by_refresh_token(refresh_token):
    """
    Returns a user object from the database given an update token
    """
    return User.query.filter(User.refresh_token == refresh_token).first()


def verify_credentials(email, password):
    """
    Returns true if the credentials match, otherwise returns false
    """
    possible_user = get_user_by_email(email)

    if possible_user is None:
        return False, None

    return possible_user.verify_password(password), possible_user

def create_user(username,email, password):
    """
    Creates a User object in the database

    Returns if creation was successful, and the User object
    """
    possible_user = get_user_by_email(email)
    if possible_user is not None:
        return False, possible_user
    
    user = User(username=username,email=email,password=password)
    db.session.add(user)
    db.session.commit()
    return True, user 

def renew_session(refresh_token):
    """
    Renews a user's session token
    
    Returns the User object
    """
    possible_user = get_user_by_refresh_token(refresh_token)
    if possible_user is None:
        raise Exception("Invalid refresh token")
    possible_user.renew_session()
    db.session.commit()
    return possible_user
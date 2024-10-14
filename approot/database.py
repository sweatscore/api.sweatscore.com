"""
    The database module.
    Example: Adding an index to a table:
        __table_args__ = (Index(None, 'facebook_id', 'active', unique=True), )
"""

from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import Boolean, BigInteger, String, DateTime, ForeignKey

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

import library as applib

engine = None


class Base(DeclarativeBase): pass


class UserStatus(Base):
    """ The status of a Sweatscore user record """

    __tablename__ = 'user_statuses'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    description: Mapped[str] = mapped_column(String(250))


class SweatscoreUser(Base):
    """ The Sweatscore user account table """

    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    status_id: Mapped['UserStatus'] = mapped_column(ForeignKey('user_statuses.id'))
    email_address: Mapped[str] = mapped_column(String(250))
    password: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(DateTime)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)


class ReturnCode(Base):
    """ Status codes and descriptions that can be returned to the front-end client """

    __tablename__ = 'return_codes'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(8), unique=True)
    message: Mapped[str] = mapped_column(String(500))


class EmailCode(Base):
    """
        Temporary codes that are emailed when establishing a new user account or email address.
    """

    __tablename__ = 'email_codes'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    code: Mapped[str] = mapped_column(String(8), unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime)
    
    user: Mapped['SweatscoreUser'] = relationship()


def get_db_session():
    """ Returns a database session """

    session = SessionMaker()

    try:
        yield session
    finally:
        session.close()


def create_connection_string():
    """ Returns a properly formatted connection string for connection to the database """

    connection_params = applib.get_config_section('database')

    connection_string = (
        f"{connection_params['dialect_driver']}://"
        f"{connection_params['username']}:"
        f"{connection_params['password']}"
        f"@{connection_params['host']}"
        f":{connection_params['port']}"
        f"/{connection_params['database']}"
    )

    return connection_string


if engine is None:
    connection_string = create_connection_string()

    engine = create_engine(connection_string, echo=applib.DEBUG)

    SessionMaker = sessionmaker(autocommit=False, autoflush=False, bind=engine)

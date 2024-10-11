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
    relationship,
)

import library as applib


class Base(DeclarativeBase): pass


class SweatscoreUser(Base):
    """ The main Sweatscore user account table """

    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email_address: Mapped[str] = mapped_column(String(250))
    password: Mapped[str] = mapped_column(String(200))
    created_at: Mapped[datetime] = mapped_column(DateTime)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)


# class FacebookUser(Base):
#     """ The FacebookUser model/facebook_users table """

#     __tablename__ = 'facebook_users'

#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     facebook_id: Mapped[str] = mapped_column(String(50), unique=True)
#     access_token: Mapped[str] = mapped_column(String(500))
#     access_token_expiration: Mapped[datetime] = mapped_column(DateTime, nullable=True)
#     created_at: Mapped[datetime] = mapped_column(DateTime)
#     updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

#     digiads_user: Mapped["DigiAdsUser"] = relationship(back_populates="facebook_user", cascade="all, delete-orphan")

#     def __repr__(self):
#         return f"FacebookUser(id={self.id!r}, facebook_id={self.facebook_id!r})"


# class DigiAdsUser(Base):
#     """ The DigiAdsUser model/digiads_users table """

#     __tablename__ = 'digiads_users'

#     id: Mapped["FacebookUser"] = mapped_column(ForeignKey("facebook_users.id"), primary_key=True)
#     email: Mapped[str] = mapped_column(String(250))
#     name: Mapped[str] = mapped_column(String(250))
#     business_name: Mapped[str] = mapped_column(String(250))
#     phone_number: Mapped[str] = mapped_column(String(25))
#     website: Mapped[str] = mapped_column(String(250))
#     active: Mapped[bool] = mapped_column(Boolean(), default=True)
#     created_at: Mapped[datetime] = mapped_column(DateTime)
#     updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

#     facebook_user: Mapped["FacebookUser"] = relationship(back_populates="digiads_user")
#     user_logs: Mapped[list["UserLog"]] = relationship(back_populates="digiads_user", cascade="all, delete-orphan")

#     def __repr__(self):
#         return f"DigiAdsUser(id={self.id!r}, name={self.name!r})"


# class UserLog(Base):
#     """ The UserLog model/user_logs table """

#     __tablename__ = 'user_logs'

#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
#     digiads_user_id: Mapped["DigiAdsUser"] = mapped_column(ForeignKey("digiads_users.id"), index=True)
#     log_entry: Mapped[str] = mapped_column(String(250))
#     created_at: Mapped[datetime] = mapped_column(DateTime, index=True)

#     digiads_user: Mapped["DigiAdsUser"] = relationship(back_populates="user_logs")

#     def __repr__(self):
#         return f"UserLog(user_id={self.user_id!r}, log_entry={self.log_entry!r})"


# class FacebookAdAccount(Base):
#     """ Facebook ad accounts belonging to a user """

#     __tablename__ = 'facebook_ad_accounts'

#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     digiads_user_id: Mapped["DigiAdsUser"] = mapped_column(ForeignKey("digiads_users.id"), index=True)
#     ad_account_id: Mapped[str] = mapped_column(String(30), unique=True)
#     ad_account_name: Mapped[str] = mapped_column(String(100))
#     facebook_ad_account_id: Mapped[str] = mapped_column(String(30))
#     created_at: Mapped[datetime] = mapped_column(DateTime)
#     updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)


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


connection_string = create_connection_string()

engine = create_engine(connection_string, echo=applib.DEBUG)

SessionMaker = sessionmaker(autocommit=False, autoflush=False, bind=engine)

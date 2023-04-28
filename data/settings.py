import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Settings(SqlAlchemyBase):
    __tablename__ = 'settings'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    bg_color = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    text_color = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    theme = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    city = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    user = orm.relationship('User')


    def __repr__(self):
        return f"{self.__class__.__name__} {self.bg_color} {self.text_color} {self.theme}  {self.city}"
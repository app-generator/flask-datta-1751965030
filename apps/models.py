# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from email.policy import default
from apps import db
from sqlalchemy.exc import SQLAlchemyError
from apps.exceptions.exception import InvalidUsage
import datetime as dt
from sqlalchemy.orm import relationship
from enum import Enum

class CURRENCY_TYPE(Enum):
    usd = 'usd'
    eur = 'eur'

class Product(db.Model):

    __tablename__ = 'products'

    id            = db.Column(db.Integer,      primary_key=True)
    name          = db.Column(db.String(128),  nullable=False)
    info          = db.Column(db.Text,         nullable=True)
    price         = db.Column(db.Integer,      nullable=False)
    currency      = db.Column(db.Enum(CURRENCY_TYPE), default=CURRENCY_TYPE.usd, nullable=False)

    date_created  = db.Column(db.DateTime,     default=dt.datetime.utcnow())
    date_modified = db.Column(db.DateTime,     default=db.func.current_timestamp(),
                                               onupdate=db.func.current_timestamp())
    
    def __init__(self, **kwargs):
        super(Product, self).__init__(**kwargs)

    def __repr__(self):
        return f"{self.name} / ${self.price}"

    @classmethod
    def find_by_id(cls, _id: int) -> "Product":
        return cls.query.filter_by(id=_id).first() 

    def save(self) -> None:
        try:
            db.session.add(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.close()
            error = str(e.__dict__['orig'])
            raise InvalidUsage(error, 422)

    def delete(self) -> None:
        try:
            db.session.delete(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.close()
            error = str(e.__dict__['orig'])
            raise InvalidUsage(error, 422)
        return


#__MODELS__
class Users(db.Model):

    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)

    #__Users_FIELDS__
    id = db.Column(db.Integer, nullable=True)
    username = db.Column(db.String(255),  nullable=True)
    password = db.Column(db.String(255),  nullable=True)
    email = db.Column(db.String(255),  nullable=True)
    email_verified = db.Column(db.Boolean, nullable=True)
    is_enabled = db.Column(db.Boolean, nullable=True)
    is_admin = db.Column(db.Boolean, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    lastlog_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    comments = db.Column(db.Text, nullable=True)

    #__Users_FIELDS__END

    def __init__(self, **kwargs):
        super(Users, self).__init__(**kwargs)


class Posts(db.Model):

    __tablename__ = 'Posts'

    id = db.Column(db.Integer, primary_key=True)

    #__Posts_FIELDS__
    services = db.Column(db.Text, nullable=True)
    message = db.Column(db.Text, nullable=True)
    views = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    is_visible = db.Column(db.Boolean, nullable=True)

    #__Posts_FIELDS__END

    def __init__(self, **kwargs):
        super(Posts, self).__init__(**kwargs)


class Comments(db.Model):

    __tablename__ = 'Comments'

    id = db.Column(db.Integer, primary_key=True)

    #__Comments_FIELDS__
    subject = db.Column(db.Text, nullable=True)
    message = db.Column(db.Text, nullable=True)
    services_used = db.Column(db.Text, nullable=True)
    rating_overall = db.Column(db.Integer, nullable=True)
    is_visible = db.Column(db.Boolean, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    views = db.Column(db.Integer, nullable=True)

    #__Comments_FIELDS__END

    def __init__(self, **kwargs):
        super(Comments, self).__init__(**kwargs)



#__MODELS__END

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy import String, Integer, DateTime, TIMESTAMP, ForeignKey, PrimaryKeyConstraint, UniqueConstraint


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    # Añadir la restricción UNIQUE
    __table_args__ = (
        UniqueConstraint('email', name='user_email_key'),
    )

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }


class People(db.Model):
    __tablename__ = 'peoples'
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    name = db.Column(String(100), unique=True, nullable=False)
    url = db.Column(String(500), unique=True, nullable=False)


class Planets(db.Model):
    __tablename__ = 'planets'
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    name = db.Column(String(100), unique=True, nullable=False)
    url = db.Column(String(500), unique=True, nullable=False)

    # Añadir las restricciones UNIQUE
    __table_args__ = (
        UniqueConstraint('name', name='planets_name_key'),
        UniqueConstraint('url', name='planets_url_key'),
    )


class Favorite_Planets(db.Model):
    __tablename__ = 'favorite_planets'
    id_planet = db.Column(Integer, ForeignKey('planets.id'), primary_key=True)
    id_user = db.Column(Integer, ForeignKey('users.id'), primary_key=True)
    created = db.Column(DateTime(timezone=True),
                        default=func.now(), nullable=False)
    # Añadir la clave primaria compuesta
    __table_args__ = (
        PrimaryKeyConstraint('id_user', 'id_planet',
                             name='favorite_planets_pk'),
    )


class Favorite_People(db.Model):
    __tablename__ = 'favorite_people'
    id_user = db.Column(Integer, ForeignKey('users.id'), primary_key=True)
    id_people = db.Column(Integer, ForeignKey('peoples.id'), primary_key=True)
    created = db.Column(DateTime(timezone=True),
                        default=func.now(), nullable=False)
    # Añadir la clave primaria compuesta
    __table_args__ = (
        PrimaryKeyConstraint('id_people', 'id_user',
                             name='favorite_people_pk'),
    )

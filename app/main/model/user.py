import datetime
import logging
import uuid
from enum import Enum

from werkzeug.security import check_password_hash, generate_password_hash

from .. import db
from ..util.helper import convert_to_local_time, create_token, is_valid_email

# Set up logging
# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    deleted_at = db.Column(db.DateTime, default=None, nullable=True)

    def __repr__(self):
        return f"<User(username={self.username}, email={self.email})>"

    def serialize(self):
        created_at = convert_to_local_time(self.created_at)
        updated_at = convert_to_local_time(self.updated_at)
        return {
            "public_id": self.public_id,
            "username": self.username,
            "email": self.email,
            "created_at": created_at.isoformat() if self.created_at else None,
            "updated_at": updated_at.isoformat() if self.updated_at else None,
            "role": self.role,
            "status": self.status,
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def get_all_users(self, page, count):
        try:
            offset = (page - 1) * count
            users = self.query.limit(count).offset(offset).all()
            return [user.serialize() for user in users]
        except Exception as e:
            raise e

    def register_user(self, data):
        try:
            email = data.get("email")
            if not is_valid_email(email):
                raise Exception("The email is invalid")
            user = self.query.filter_by(email=email).first()
            if user:
                raise Exception("This email has already been registered")

            new_user = User(
                public_id=str(uuid.uuid4()),
                username=data.get("username"),
                email=email,
                password=generate_password_hash(data.get("password")),
                role=data.get("role", "user"),
                status=data.get("status", "active"),
                created_at=datetime.datetime.utcnow(),
                updated_at=datetime.datetime.utcnow(),
            )
            new_user.save()
            return new_user.serialize()
        except Exception as e:
            raise e

    # please never return this
    def serialize_entire_data(self):
        return {
            "id": self.id,
            "public_id": self.public_id,
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "role": self.role,
            "status": self.status,
        }

    def user_auth(self, data):
        try:
            user = self.query.filter_by(email=data.get("email")).first()
            if not user:
                raise Exception("User not found. Invalid ID")

            user_data = user.serialize_entire_data()
            if check_password_hash(user_data["password"], data.get("password")):
                return create_token(user_data)
            else:
                raise Exception("Incorrect password. Please try again")

        except Exception as e:
            raise e

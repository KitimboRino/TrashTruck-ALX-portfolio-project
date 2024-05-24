from app import db
from sqlalchemy.orm import mapped_column
from sqlalchemy import String, Integer


class User(db.Model):
    id = mapped_column(Integer, primary_key=True)
    username = mapped_column(String(64), index=True, unique=True)
    email = mapped_column(String(120), index=True, unique=True)
    password_hash = mapped_column(String(256))

    def set_password(self, password):
        from werkzeug.security import generate_password_hash
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

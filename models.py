from app import db
from sqlalchemy.orm import mapped_column
from sqlalchemy import String, Integer


class User(db.Model):
    """
    User model for storing user details.
    
    Attributes:
        id (Integer): The primary key for the user.
        username (String): The unique username of the user.
        email (String): The unique email address of the user.
        password_hash (String): The hashed password for the user.
    """
    id = mapped_column(Integer, primary_key=True)  # Primary key column
    username = mapped_column(String(64), index=True, unique=True)  # Username column, indexed and unique
    email = mapped_column(String(120), index=True, unique=True)  # Email column, indexed and unique
    password_hash = mapped_column(String(256))  # Password hash column

    def set_password(self, password):
        """
        Hashes the user's password and stores it in the password_hash field.

        Args:
            password (str): The plaintext password to be hashed.
        """
        from werkzeug.security import generate_password_hash  # Import password hashing function
        self.password_hash = generate_password_hash(password)  # Generate and set the password hash

    def check_password(self, password):
        """
        Verifies the user's password against the stored hash.

        Args:
            password (str): The plaintext password to be verified.

        Returns:
            bool: True if the password matches the hash, False otherwise.
        """
        from werkzeug.security import check_password_hash  # Import password hash verification function
        return check_password_hash(self.password_hash, password)  # Check and return the password match result

    def __repr__(self):
        """
        Returns a string representation of the User instance.

        Returns:
            str: A string in the format '<User {username}>'.
        """
        return '<User {}>'.format(self.username)  # Return the string representation

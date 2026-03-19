"""
Configuration module.

Loads environment variables and exposes configuration constants
used across the application (e.g., JWT settings).
"""
from dotenv import load_dotenv
import os

load_dotenv()

# Secret key used for JWT signing
SECRET_KEY = os.getenv("SECRET_KEY")

# Algorithm used for JWT encoding/decoding
ALGORITHM = os.getenv("ALGORITHM")

# Token expiration time in minutes
ACCESS_TOKEN_EXPIRE_MIN = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))




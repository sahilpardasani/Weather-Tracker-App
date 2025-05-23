from sqlalchemy import create_engine, Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from datetime import datetime
from passlib.hash import bcrypt

# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemy setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# ==========================
# MODELS
# ==========================

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    password = Column(String(200), nullable=False)  # hashed password
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

class SearchHistory(Base):
    __tablename__ = 'search_history'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    city_name = Column(String(100), nullable=False)
    searched_at = Column(TIMESTAMP, default=datetime.utcnow)

# ==========================
# UTILITY FUNCTIONS
# ==========================

def get_or_create_user(session, username, raw_password):
    """
    Returns existing user or creates a new one with hashed password.
    """
    user = session.query(User).filter_by(username=username).first()
    if not user:
        hashed_pw = bcrypt.hash(raw_password)
        user = User(username=username, password=hashed_pw)
        session.add(user)
        session.commit()
        session.refresh(user)
    return user

def create_user(session, username, raw_password):
    """
    Creates a new user with hashed password.
    """
    hashed_pw = bcrypt.hash(raw_password)
    user = User(username=username, password=hashed_pw)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def authenticate_user(session, username, raw_password):
    """
    Authenticates a user by verifying the provided password
    against the hashed password stored in the database.
    """
    user = session.query(User).filter_by(username=username).first()
    if user and bcrypt.verify(raw_password, user.password):
        return user
    return None

def save_search(session, user_id, city_name):
    """
    Saves a new weather search record for the user.
    """
    entry = SearchHistory(user_id=user_id, city_name=city_name)
    session.add(entry)
    session.commit()

def get_recent_searches(session, user_id):
    """
    Retrieves the user's recent search history in descending order.
    """
    return session.query(SearchHistory)\
        .filter_by(user_id=user_id)\
        .order_by(SearchHistory.searched_at.desc())\
        .all()

def clear_searches(session, user_id):
    """
    Deletes all weather search records for the given user.
    """
    session.query(SearchHistory).filter_by(user_id=user_id).delete()
    session.commit()

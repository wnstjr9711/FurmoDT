from sqlalchemy import Column, Integer, VARCHAR
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    user_id = Column(VARCHAR(45), primary_key=True)
    user_password = Column(VARCHAR(1000), nullable=False)
    user_authority_level = Column(Integer, nullable=False)

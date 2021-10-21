from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.schema import Base, User
import sqlalchemy.exc
import os


class SQLAlchemy:
    def __init__(self):
        self.engine = create_engine('mysql+pymysql://root:{}@{}/furmodt'.format(os.environ.get("DATABASE_PASSWORD"),
                                                                                os.environ.get("DATABASE_URL")),
                                    echo=True)
        self.session = sessionmaker(bind=self.engine)()

    def create_table(self):
        Base.metadata.create_all(self.engine)

    def register_user(self, user_id, user_pw, user_auth_level):
        try:
            self.session.add(User(user_id=user_id, user_password=user_pw, user_authority_level=user_auth_level))
            self.session.commit()
        except sqlalchemy.exc.IntegrityError:
            print('id already exists')

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.schema import Base, User
import sqlalchemy.exc
import bcrypt
import os


class SQLAlchemy:
    def __init__(self):
        self.engine = create_engine('mysql+pymysql://root:{}@{}/furmodt'.format(os.environ.get("DATABASE_PASSWORD"),
                                                                                os.environ.get("DATABASE_URL")))
        # echo=True
        self.session = sessionmaker(bind=self.engine)()

    def create_table(self):
        Base.metadata.create_all(self.engine)

    def user_register(self, user_id, user_pw, user_auth_level):
        try:
            self.session.add(User(user_id=user_id, user_password=bcrypt.hashpw(user_pw.encode('utf-8'), bcrypt.gensalt()), user_authority_level=user_auth_level))
            self.session.commit()
        except sqlalchemy.exc.IntegrityError:
            print('id already exists')

    def user_login(self, user_id, user_pw):
        msg, ret = None, None
        try:
            user = self.session.query(User).filter(User.user_id == user_id).first()
            hashed_pw = user.user_password
            if bcrypt.checkpw(user_pw.encode('utf-8'), bytes(hashed_pw, encoding='utf-8')):
                msg = 'success'
                ret = user.user_authority_level
            else:
                msg = 'wrong password'
        except AttributeError:
            msg = 'id not exists'
        finally:
            return msg, ret

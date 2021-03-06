import logging
import os

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, SmallInteger, or_

from exception_handler import Error
from models.utils import UserRole, salted_password, FileType, FileShare, get_readable_size, current_time
from settings import BASE_FILE_PATH, DOWNLOAD_URL_PREFIX

logger = logging.getLogger(__name__)

db = SQLAlchemy()


class Base(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    created_time = Column(Integer, default=current_time)

    @classmethod
    def create(cls, data):
        m = cls(**data)
        m.save()
        return m

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get(cls, **kwargs):
        m = cls.query.filter_by(**kwargs).first()
        return m

    @classmethod
    def getOr404(cls, **kwargs):
        m = cls.get(**kwargs)
        if m is None:
            raise Error.not_found
        return m

    @classmethod
    def get_list(cls, **kwargs):
        ms = cls.query.filter_by(**kwargs).all()
        return ms

    def update(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.save()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def update_by_id(cls, pk, **kwargs):
        m = cls.get(id=pk)
        m.update(**kwargs)

    @classmethod
    def delete_by_id(cls, pk):
        m = cls.get(id=pk)
        m.delete()


class User(Base):
    name = Column(String(20), nullable=False, unique=True)
    password = Column(String(64), nullable=False)
    role = Column(SmallInteger, default=UserRole.NORMAL)
    avatar = Column(String(256), nullable=True)

    @classmethod
    def register(cls, name, password):
        try:
            cls.create(dict(name=name, password=salted_password(password)))
            return True
        except Exception as e:
            logger.error("Register Error: {}".format(e))
            return False

    @classmethod
    def login(cls, name, password):
        return cls.get(name=name, password=salted_password(password))

    @classmethod
    def authenticate(cls, name, password):
        u = cls.get(name=name, password=salted_password(password))
        if u is not None:
            return True
        return False

    @property
    def is_admin(self):
        return self.role == UserRole.ADMIN

    def to_dict(self):
        return dict(
            userId=self.id,
            isAdmin=self.is_admin,
            username=self.name,
            role=self.role,
            avatar=self.avatar,
        )


class File(Base):
    name = Column(String(100), nullable=False)
    uuid = Column(String(36), nullable=False)
    type = Column(SmallInteger, default=FileType.UNKNOWN)
    md5 = Column(String(60), nullable=False, index=True)
    path = Column(String(72), nullable=False)
    share = Column(SmallInteger, default=FileShare.EXCLUSIVE)
    size = Column(Integer, nullable=False)
    upload_user = Column(Integer, nullable=False)

    @property
    def username(self):
        u_id = self.upload_user
        u = User.get(id=u_id)
        if u is not None:
            return u.name
        return None

    @property
    def url(self):
        return DOWNLOAD_URL_PREFIX + self.path[len(BASE_FILE_PATH):]

    @property
    def readable_size(self):
        return get_readable_size(self.size)

    @classmethod
    def get_list_not_admin(cls, u_id):
        fs = cls.query.filter(or_(cls.upload_user == u_id, cls.share < FileShare.EXCLUSIVE)).all()
        return fs

    def remove(self):
        try:
            os.remove(os.path.join(BASE_FILE_PATH, self.path))
        except Exception:
            pass
        self.delete()

    def to_dict(self):
        return dict(
            id=self.id,
            name=self.name,
            uuid=self.uuid,
            type=self.type,
            path=self.path,
            share=self.share < FileShare.EXCLUSIVE,
            size=self.readable_size,
            uploader=self.upload_user,
            create_time=self.created_time,
        )

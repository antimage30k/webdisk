import time
from hashlib import sha256

from settings import SALT


class UserRole:
    ADMIN = 1
    NORMAL = 2
    INVITED = 3
    GUEST = 4


class DefaultUserId:
    ADMIN = 1
    GUEST = -1


class FileType:
    UNKNOWN = 0
    PICTURE = 1
    DOCUMENT = 2
    PACKAGE = 3


class FileShare:
    PUBLIC = 1
    AUTHENTICATED = 2
    EXCLUSIVE = 3


def salted_password(raw):
    salted = raw + SALT
    return sha256(salted.encode('ascii')).hexdigest()


def get_readable_size(size: int):
    if size < 1024:
        return '{}B'.format(size)

    kb = size / 1024
    if kb < 1024:
        return '{:.2f}KB'.format(kb)

    mb = kb / 1024
    if mb < 1024:
        return '{:.2f}MB'.format(mb)

    gb = mb / 1024
    if gb < 1024:
        return '{:.2f}GB'.format(gb)
    return size


def current_time():
    return int(time.time())

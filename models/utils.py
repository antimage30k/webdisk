from settings import SALT
from hashlib import sha256


class UserRole:
    ADMIN = 1
    NORMAL = 2
    INVITED = 3
    GUEST = 4


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

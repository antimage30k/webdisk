import os
import uuid
from hashlib import md5

from settings import BASE_FILE_PATH


def get_local_file_md5(path):
    m = md5()
    with open(path, 'rb') as f:
        while True:
            data = f.read(4194304)  # 4096 * 1024 byte = 4Mb
            if not data:
                break
            m.update(data)
        file_md5 = m.hexdigest()
    return file_md5


def get_uuid():
    _uuid = str(uuid.uuid4())
    _dir = os.path.join(BASE_FILE_PATH, _uuid[0])
    if not os.path.exists(_dir):
        os.makedirs(_dir)
    return _uuid

import os
from hashlib import md5

from flask import render_template, abort, Blueprint, request, jsonify, Response
from werkzeug.datastructures import FileStorage

from disk.file import get_uuid
from models.base import File
from models.utils import FileShare, UserRole
from routes import current_user, guest

disk = Blueprint('disk', __name__)


@disk.route('/upload', methods=['POST'])
def upload():
    file: FileStorage = request.files['file']
    file_size = request.form['size']
    archive = save_file(file, file_size)

    ret = dict(
        filename=archive.name,
        size=archive.size,
        url=archive.path,
    )
    return jsonify(ret)


@disk.route('/disk')
def index():
    u = current_user()
    if u is guest:
        files = File.get_list(share=FileShare.PUBLIC)
    elif u.role == UserRole.ADMIN:
        files = File.get_list()
    else:
        files = File.get_list_not_admin(u.id)
    return render_template('upload.html', files=files)


def get_file_storage_md5(file: FileStorage):
    _md5 = md5()
    while True:
        data = file.stream.read(1024 * 1024)
        if not data:
            break
        _md5.update(data)
    file.stream.seek(0)  # 将文件操作标记移回开头
    return _md5.hexdigest()


def save_file(file: FileStorage, file_size):
    u = current_user()
    uid = u.id

    form = dict(
        name=file.filename,
        size=file_size,
        upload_user=uid,
    )

    # 用md5值判断文件是否已存在
    _md5 = get_file_storage_md5(file)

    f: File = File.get(md5=_md5)

    # 文件不存在, 存储
    if f is None:
        suffix = file.filename.rsplit('.', 1)[1]
        _uuid, _dir = get_uuid()
        form.update(dict(
            uuid=_uuid,
            md5=_md5,
            path=os.path.join(_dir, _uuid + '.' + suffix),
        ))
        archive = File.create(form)
        file.save(archive.path)

    # 文件已存在，新建数据库条目，但不用存储文件
    else:
        if f.upload_user == uid:
            abort(Response('文件已存在'))

        form.update(dict(
            uuid=f.uuid,
            md5=f.md5,
            path=f.path,
        ))
        archive = File.create(form)

    return archive


@disk.route('/delete/<file_id>', methods=['delete'])
def delete(file_id):
    u = current_user()
    f: File = File.get(id=file_id)

    if u == guest:
        abort(401)

    if (not u.isadmin) and (f.upload_user != u.id):  # 不是该用户上传的文件
        abort(401)

    files = File.get_list(md5=f.md5)
    if len(files) == 1:  # 只有该用户拥有，删除实体文件
        f.remove()
    else:
        f.delete()

    return jsonify(f'deleted {f.name}')

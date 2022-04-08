import os
from hashlib import md5

from flask import abort, Blueprint, request, jsonify, Response, send_file
from werkzeug.datastructures import FileStorage

from disk.file import get_uuid
from exception_handler import Error
from models.base import File, User
from models.utils import FileShare, UserRole
from routes import current_user, guest, escape_filename, login_required
from settings import BASE_FILE_PATH

disk = Blueprint('disk', __name__)


@disk.route('/upload', methods=['POST'])
@login_required
def upload():
    file: FileStorage = request.files['file']
    file_size = request.form['size']
    archive = save_file(file, file_size)

    ret = dict(
        time=str(archive.created_time),
        filename=archive.name,
        size=archive.readable_size,
        url=archive.url,
    )
    return jsonify(ret)


@disk.route('/upload/multi', methods=['POST'])
@login_required
def upload_multi():
    file: FileStorage = request.files['file']
    archive = save_file(file)
    return jsonify(archive.to_dict())


@disk.route('/')
def index():
    u = current_user()
    if u is guest:
        files = File.get_list(share=FileShare.PUBLIC)
    elif u.role == UserRole.ADMIN:
        files = File.get_list()
    else:
        files = File.get_list_not_admin(u.id)
    result = [f.to_dict() for f in files]
    return jsonify(result)


@disk.route('/delete/<file_id>', methods=['delete'])
def delete(file_id):
    u: User = current_user()
    f: File = File.get(id=file_id)

    if u is guest:
        raise Error.not_authorized

    _check_admin_or_uploader(u, f)

    files = File.get_list(md5=f.md5)
    if len(files) == 1:  # 只有该用户拥有，删除实体文件
        f.remove()
    else:
        f.delete()

    return jsonify(dict(
        id=f.id,
        uuid=f.uuid,
        name=f.name,
    ))


@disk.route("/download/<file_id>", methods=['GET'])
def download(file_id):
    f: File = File.get(id=file_id)
    return send_file(os.path.join(BASE_FILE_PATH, f.path), as_attachment=True, attachment_filename=f.name)


@disk.route('/share/set', methods=['POST'])
@login_required
def publish():
    file_id = request.json['id']
    share: bool = request.json['share']
    u: User = current_user()
    f: File = File.get(id=file_id)
    _check_admin_or_uploader(u, f)
    if share is False:
        f.share = FileShare.EXCLUSIVE
    elif share is True:
        f.share = FileShare.PUBLIC
    f.save()
    return jsonify(f.to_dict())


def get_file_storage_md5(file: FileStorage):
    _md5 = md5()
    while True:
        data = file.stream.read(1024 * 1024)
        if not data:
            break
        _md5.update(data)
    file.stream.seek(0)  # 将文件操作标记移回开头
    return _md5.hexdigest()


def save_file(file: FileStorage, file_size=None):
    u = current_user()
    uid = u.id

    form = dict(
        name=escape_filename(file.filename),
        size=file_size,
        upload_user=uid,
    )

    # 用md5值判断文件是否已存在
    _md5 = get_file_storage_md5(file)

    f: File = File.get(md5=_md5)

    # 文件不存在, 存储
    if f is None:
        _uuid = get_uuid()
        path = os.path.join(_uuid[0], _uuid)
        form.update(dict(
            uuid=_uuid,
            md5=_md5,
            path=path,
        ))
        absolute_path = os.path.join(BASE_FILE_PATH, path)
        file.save(absolute_path)
        if file_size is None:
            form.update(size=os.path.getsize(absolute_path))
        archive = File.create(form)

    # 文件已存在，新建数据库条目，但不用存储文件
    else:
        if f.upload_user == uid:
            abort(Response("File exists"))

        form.update(dict(
            uuid=f.uuid,
            md5=f.md5,
            path=f.path,
            size=f.size,
        ))
        archive = File.create(form)

    return archive


def _check_admin_or_uploader(u: User, f: File):
    if (not u.is_admin) and (f.upload_user != u.id):  # 不是该用户上传的文件
        raise Error.not_authorized

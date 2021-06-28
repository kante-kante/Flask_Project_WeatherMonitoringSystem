import time
import uuid
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('device', __name__, url_prefix='/device')


# 정보
def get_device(id, check_author=True):
    device = (
        get_db()
        .execute(
            'SELECT d.id, d.name, d.api_key, d.created, d.updated, d.user_id, u.username'
            ' FROM device d JOIN user u ON d.user_id = u.id'
            ' WHERE d.id = ?',
            (id,),
        )
        .fetchone()
    )

    if device is None:
        abort(404, "정보가 존재하지 않습니다.")

    if check_author and device['user_id'] != g.user['id']:
        abort(403)

    return device


# 목록
@bp.route('/list')
@login_required
def lists():
    db = get_db()
    devices = None

    if g.user['grade'] == '관리자':
        devices = db.execute(
            'SELECT d.id, d.name, d.api_key, d.created, d.updated, d.user_id, u.username'
            ' FROM device d JOIN user u ON d.user_id = u.id'
            ' ORDER BY d.created DESC'
        ).fetchall()
    else:
        devices = db.execute(
            'SELECT d.id, d.name, d.api_key, d.created, d.updated, d.user_id, u.username'
            ' FROM device d JOIN user u ON d.user_id = u.id'
            ' WHERE d.user_id = ?'
            ' ORDER BY d.created DESC',
            (g.user['id'],),
        ).fetchall()

    return render_template('device/list.html', title='기기', list=True, work='device', profile=g.user, devices=devices)


# 보기
@bp.route('/view/<int:id>')
@login_required
def view(id):
    device = get_device(id, False)
    return render_template('device/view.html', title='기기', profile=g.user, device=device)


# 추가
@bp.route('/add', methods=('GET', 'POST'))
@login_required
def add():
    if request.method == 'POST':
        name = request.form['name']
        error = None

        if not name:
            error = '이름은 필수입니다.'

        if error is not None:
            flash(error)
        else:
            now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            api_key = str(uuid.uuid4())

            db = get_db()
            db.execute(
                'INSERT INTO device (name, user_id, api_key, created, updated) VALUES (?, ?, ?, ?, ?)',
                (name, g.user['id'], api_key, now, now),
            )
            db.commit()
            return redirect(url_for('device.lists'))

    return render_template('device/add.html', title='기기', profile=g.user)


# 수정
@bp.route('/edit/<int:id>', methods=('GET', 'POST'))
@login_required
def edit(id):
    device = get_device(id, True)

    if request.method == 'POST':
        name = request.form['name']
        error = None

        if not name:
            error = '이름은 필수입니다.'

        if error is not None:
            flash(error)
        else:
            now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

            db = get_db()
            db.execute(
                'UPDATE device SET name = ?, updated = ? WHERE id = ?', (name, now, id)
            )
            db.commit()
            return redirect('/device/view/{}'.format(id))

    return render_template('device/edit.html', title='기기', profile=g.user, device=device)


# 삭제
@bp.route('/delete', methods=("POST",))
@login_required
def delete():
    id = request.form['id']
    get_device(id, True)
    db = get_db()
    db.execute('DELETE FROM device WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('device.lists'))

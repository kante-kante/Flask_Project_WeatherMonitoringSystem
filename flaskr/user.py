import time
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from werkzeug.security import generate_password_hash
from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('user', __name__, url_prefix='/user')


# 정보
def get_user(id):
    user = (
        get_db()
        .execute(
            'SELECT id, username, phone, email, password, grade, created, updated'
            ' FROM user'
            ' WHERE id = ?',
            (id,),
        )
        .fetchone()
    )

    if user is None:
        abort(404, "정보가 존재하지 않습니다.")

    if g.user['grade'] != '관리자':
        abort(403)

    return user


# 목록
@bp.route('/list')
@login_required
def lists():
    if g.user['grade'] != '관리자':
        return redirect(url_for('dashboard.forbidden'))
        #abort(403)

    db = get_db()
    users = db.execute(
        'SELECT id, username, phone, email, password, created, updated'
        ' FROM user'
        ' WHERE grade = ?'
        ' ORDER BY created DESC',
        ('사용자',),
    ).fetchall()
    return render_template('user/list.html', title='사용자', list=True, work='user', profile=g.user, users=users)


# 보기
@bp.route('/view/<int:id>')
@login_required
def view(id):
    if g.user['grade'] != '관리자':
        return redirect(url_for('dashboard.forbidden'))
        #abort(403)

    user = get_user(id)
    return render_template('user/view.html', title='사용자', profile=g.user, user=user)


# 추가
@bp.route('/add', methods=('GET', 'POST'))
@login_required
def add():
    if g.user['grade'] != '관리자':
        return redirect(url_for('dashboard.forbidden'))
        # abort(403)

    if request.method == 'POST':
        username = request.form['username']
        phone = request.form['phone']
        email = request.form['email']
        password = request.form['password']
        error = None

        if not username:
            error = '이름은 필수입니다.'
        elif not phone:
            error = '전화번호는 필수입니다.'
        elif not email:
            error = '이메일은 필수입니다.'
        elif not password:
            error = '비밀번호는 필수입니다.'

        if error is not None:
            flash(error)
        else:
            now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

            db = get_db()
            db.execute(
                'INSERT INTO user (username, phone, email, password, grade, created, updated) VALUES (?, ?, ?, ?, ?, ?, ?)',
                (username, phone, email, generate_password_hash(password), '사용자', now, now)
            )
            db.commit()
            return redirect(url_for('user.lists'))

    return render_template('user/add.html', title='사용자', profile=g.user)


# 수정
@bp.route('/edit/<int:id>', methods=('GET', 'POST'))
@login_required
def edit(id):
    if g.user['grade'] != '관리자':
        return redirect(url_for('dashboard.forbidden'))
        # abort(403)

    user = get_user(id)

    if request.method == 'POST':
        username = request.form['username']
        phone = request.form['phone']
        email = request.form['email']
        error = None

        if not username:
            error = '이름은 필수입니다.'
        elif not phone:
            error = '전화번호는 필수입니다.'
        elif not email:
            error = '이메일은 필수입니다.'

        if error is not None:
            flash(error)
        else:
            now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

            db = get_db()
            db.execute(
                'UPDATE user SET username = ?, phone = ?, email = ?, updated = ? WHERE id = ?', (username, phone, email, now, id)
            )
            db.commit()
            return redirect('/user/view/{}'.format(id))

    return render_template('user/edit.html', title='사용자', profile=g.user, user=user)


# 비밀번호 수정
@bp.route('/password/<int:id>', methods=('GET', 'POST'))
@login_required
def password(id):
    if g.user['grade'] != '관리자':
        return redirect(url_for('dashboard.forbidden'))
        # abort(403)

    user = get_user(id)

    if request.method == 'POST':
        password = request.form['password']
        error = None

        if not password:
            error = '비밀번호는 필수입니다.'

        if error is not None:
            flash(error)
        else:
            now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

            db = get_db()
            db.execute(
                'UPDATE user SET password = ?, updated = ? WHERE id = ?', (generate_password_hash(password), now, id)
            )
            db.commit()
            return redirect('/user/view/{}'.format(id))

    return render_template('user/password.html', title='사용자', profile=g.user, user=user)


# 삭제
@bp.route('/delete', methods=("POST",))
@login_required
def delete():
    if g.user['grade'] != '관리자':
        return redirect(url_for('dashboard.forbidden'))
        # abort(403)

    id = request.form['id']
    get_user(id)
    db = get_db()
    db.execute('DELETE FROM user WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('user.lists'))

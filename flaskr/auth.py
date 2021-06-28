import time
import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


# 로그인 여부 확인
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view


# 접속한 사용자 정보
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    # 사용자 정보 없음
    if user_id is None:
        g.user = None

    # 사용자 정보 있음
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


# 사용자 가입
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        phone = request.form['phone']
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = '이름은 필수입니다.'
        elif not phone:
            error = '전화번호는 필수입니다.'
        elif not email:
            error = '이메일은 필수입니다.'
        elif not password:
            error = '비밀번호는 필수입니다.'
        elif db.execute(
            'SELECT id FROM user WHERE email = ?', (email,)
        ).fetchone() is not None:
            error = '이메일 {} 는 이미 등록되어 있습니다.'.format(email)

        if error is None:
            now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

            db.execute(
                'INSERT INTO user (username, phone, email, password, grade, created, updated) VALUES (?, ?, ?, ?, ?, ?, ?)',
                (username, phone, email, generate_password_hash(password), '사용자', now, now)
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')


# 로그인
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE email = ?', (email,)
        ).fetchone()

        if user is None:
            error = '사용자가 없습니다.'
        elif not check_password_hash(user['password'], password):
            error = '비밀번호가 틀렸습니다.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']

            if user['grade'] == '관리자':
                return redirect(url_for('dashboard.dashboard'))
            else:
                return redirect(url_for('board.lists'))

        flash(error)

    db = get_db()
    # 관리자가 등록되어 있는지 확인 후 없으면 관리자 추가
    user = db.execute(
        'SELECT * FROM user WHERE grade = ?', ('관리자',)
    ).fetchone()

    if user is None:
        username = '홍길동'
        phone = '010-1234-5678'
        email = 'admin@test.com'
        password = 'qwer1234!@#$'
        now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        db.execute(
            'INSERT INTO user (username, phone, email, password, grade, created, updated) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (username, phone, email, generate_password_hash(password), '관리자', now, now)
        )
        db.commit()

    return render_template('auth/login.html')


# 로그아웃
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

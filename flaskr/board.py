import time
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('board', __name__, url_prefix='/board')


# 정보
def get_board(id, check_author=True):
    board = (
        get_db()
        .execute(
            'SELECT b.id, b.title, b.content, b.created, b.updated, b.user_id, u.username'
            ' FROM board b JOIN user u ON b.user_id = u.id'
            ' WHERE b.id = ?',
            (id,),
        )
        .fetchone()
    )

    if board is None:
        abort(404, "정보가 존재하지 않습니다.")

    if check_author and board['user_id'] != g.user['id']:
        abort(403)

    return board


# 목록
@bp.route('/list')
@login_required
def lists():
    db = get_db()
    boards = db.execute(
        'SELECT b.id, b.title, b.content, b.created, b.updated, b.user_id, u.username'
        ' FROM board b JOIN user u ON b.user_id = u.id'
        ' ORDER BY b.created DESC'
    ).fetchall()
    return render_template('board/list.html', title='게시판', list=True, work='board', profile=g.user, boards=boards)


# 보기
@bp.route('/view/<int:id>')
@login_required
def view(id):
    board = get_board(id, False)
    return render_template('board/view.html', title='게시판', profile=g.user, board=board)


# 추가
@bp.route('/add', methods=('GET', 'POST'))
@login_required
def add():
    if g.user['grade'] != '관리자':
        return redirect(url_for('dashboard.forbidden'))
        #abort(403)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        error = None

        if not title:
            error = '제목은 필수입니다.'
        elif not content:
            error = '내용은 필수입니다.'

        if error is not None:
            flash(error)
        else:
            now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

            db = get_db()
            db.execute(
                'INSERT INTO board (title, content, user_id, created, updated) VALUES (?, ?, ?, ?, ?)',
                (title, content, g.user['id'], now, now),
            )
            db.commit()
            return redirect(url_for('board.lists'))

    return render_template('board/add.html', title='게시판', profile=g.user)


# 수정
@bp.route('/edit/<int:id>', methods=('GET', 'POST'))
@login_required
def edit(id):
    if g.user['grade'] != '관리자':
        return redirect(url_for('dashboard.forbidden'))
        #abort(403)

    board = get_board(id, True)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        error = None

        if not title:
            error = '제목은 필수입니다.'
        elif not content:
            error = '내용은 필수입니다.'

        if error is not None:
            flash(error)
        else:
            now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

            db = get_db()
            db.execute(
                'UPDATE board SET title = ?, content = ?, updated = ? WHERE id = ?', (title, content, now, id)
            )
            db.commit()
            return redirect('/board/view/{}'.format(id))

    return render_template('board/edit.html', title='게시판', profile=g.user, board=board)


# 삭제
@bp.route('/delete', methods=("POST",))
@login_required
def delete():
    if g.user['grade'] != '관리자':
        return redirect(url_for('dashboard.forbidden'))
        #abort(403)

    id = request.form['id']
    get_board(id, True)
    db = get_db()
    db.execute('DELETE FROM board WHERE id = ?', (id,))
    db.commit()
    flash('정보가 삭제되었습니다.')
    return redirect(url_for('board.lists'))

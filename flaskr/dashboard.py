import psutil

from flask import (
    Blueprint, g, redirect, render_template, url_for
)

from flaskr.auth import login_required

bp = Blueprint('dashboard', __name__)


# 메인페이지
@bp.route('/')
@login_required
def index():
    return redirect(url_for('board.lists'))


# forbidden
@bp.route('/forbidden')
@login_required
def forbidden():
    return '권한이 없습니다.'


# 대시보드
@bp.route('/dashboard')
@login_required
def dashboard():
    cpus = psutil.cpu_percent(interval=1, percpu=True)
    cpu_values = []
    cpu_labels = []

    i = 0
    for cpu in cpus:
        cpu_values.append(cpu)
        cpu_labels.append('cpu[' + str(i) + ']')
        i = i + 1

    return render_template('dashboard/dashboard.html', title='대시보드', profile=g.user, labels=cpu_labels, values=cpu_values)

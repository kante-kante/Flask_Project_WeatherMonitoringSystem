import time
import uuid
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('monitoring', __name__, url_prefix='/monitoring')


# 목록
@bp.route('/list/<int:id>')
@login_required
def lists(id):
    db = get_db()
    monitorings = db.execute(
        'SELECT id, user_id, device_id, cpu_usage, memory_total, memory_available, memory_percent, memory_used, memory_free, disk_total, disk_percent, disk_used, disk_free, dust_ratio, h_ratio, t_ratio, created, updated'
        ' FROM monitoring'
        ' WHERE monitoring.device_id = ?'
        ' ORDER BY created DESC',
        (id,),
    ).fetchall()

    return render_template('monitoring/list.html', title='모니터링', list=True, work='monitoring', profile=g.user, monitorings=monitorings)

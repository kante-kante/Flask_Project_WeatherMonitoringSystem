import json
import time
from flask import (
    Blueprint, request, jsonify
)
from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('api', __name__, url_prefix='/api')


# 정보
def verify_api_key(api_key):
    device = (
        get_db()
        .execute('SELECT id, user_id FROM device WHERE api_key = ?', (api_key,),)
        .fetchone()
    )
    return device


# 추가
@bp.route('/add', methods=("POST",))
def add():
    data = request.get_json()
    api_key = data['api_key']
    cpu_usage = data['cpu_usage']
    memory_total = data['memory_total']
    memory_available = data['memory_available']
    memory_percent = data['memory_percent']
    memory_used = data['memory_used']
    memory_free = data['memory_free']
    disk_total = data['disk_total']
    disk_percent = data['disk_percent']
    disk_used = data['disk_used']
    disk_free = data['disk_free']
    dust_ratio = data['dust_ratio']
    h_ratio = data['h_ratio']
    t_ratio = data['t_ratio']

    # api 검증
    device = verify_api_key(api_key)

    if device is None:
        return jsonify(result='error', message='API KEY error')

    device_id = device['id']
    user_id = device['user_id']

    now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    db = get_db()
    db.execute(
        'INSERT INTO monitoring (user_id, device_id, cpu_usage, memory_total, memory_available, memory_percent, memory_used, memory_free, disk_total, disk_percent, disk_used, disk_free, dust_ratio, h_ratio, t_ratio, created, updated) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
        (
            user_id, device_id,
            cpu_usage,
            memory_total, memory_available, memory_percent, memory_used, memory_free,
            disk_total, disk_percent, disk_used, disk_free, dust_ratio, h_ratio, t_ratio,
            now, now
        ),
    )
    db.commit()
    return jsonify(result='ok')

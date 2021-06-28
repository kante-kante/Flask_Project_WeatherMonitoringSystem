import psutil
import requests
import threading


URL = 'http://127.0.0.1:5000/api/add'


def f_execute(second=5.0):
    cpu_usage = psutil.cpu_percent(interval=1, percpu=False)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('C://')

    data = {
        # "api_key": "e681ec59-2073-4f50-9874-de837899fdbd",
        "api_key": "6ccc48a9-7b68-4700-b427-24b3082cccd7",
        "cpu_usage": cpu_usage,
        "memory_total": memory[0],
        "memory_available": memory[1],
        "memory_percent": memory[2],
        "memory_used": memory[3],
        "memory_free": memory[4],
        "disk_total": disk[0],
        "disk_percent": disk[3],
        "disk_used": disk[1],
        "disk_free": disk[2],

    }
    print(data)
    headers = {'Content-type': 'application/json'}
    response = requests.post(URL, json=data, headers=headers)

    threading.Timer(second, f_execute, [second]).start()


f_execute(5.0)

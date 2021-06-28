import psutil
import requests

URL = 'http://127.0.0.1:5000/api/add'

# cpu usage
cpu_usage = psutil.cpu_percent(interval=1, percpu=False)
#print('cpu usage: ', cpu_usage)

# memory
memory = psutil.virtual_memory()
#print('')
#print(memory)
#print('memory_total: ', memory[0])
#print('memory_available: ', memory[1])
#print('memory_percent: ', memory[2])
#print('memory_used: ', memory[3])
#print('memory_free: ', memory[4])

# disk
disk = psutil.disk_usage('C://')
#print('')
#print(disk)
#print('disk_total: ', disk[0])
#print('disk_used: ', disk[1])
#print('disk_free: ', disk[2])
#print('disk_percent: ', disk[3])

data = {
    #"api_key": "e681ec59-2073-4f50-9874-de837899fdbd",
    "api_key": "5a931bed-b9dd-4c91-abfd-1a3dcb1c56c8",
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
print('')
print('code: ', response.status_code)
print(response.text)

import psutil

print("1. 개별적으로 CPU 마다 사용율 보여주기")
cpus = psutil.cpu_percent(interval=1, percpu=True)

i = 0
for cpu in cpus:
    print('cpu[' + str(i) + '] : ' + str(cpu) + '%')
    i = i + 1

print('')
print("2. 통합해서 CPU 사용율 보여주기")
cpu = psutil.cpu_percent(interval=1, percpu=False)
print(str(cpu) + '%')

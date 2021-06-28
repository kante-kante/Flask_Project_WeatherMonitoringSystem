import psutil

disks = psutil.disk_partitions()
print(disks)

"""
for disk in disks:
    # 구글드라이브 제외하기
    if disk[0] != 'G:\\':
        print(disk)
        usage = psutil.disk_usage(disk[0])
        print(usage)
        print('')

    '''
    # 모든 디스크 정보 출력하기
    print(disk)
    usage = psutil.disk_usage(disk[0])
    print(usage)
    print('')
    '''
"""

# C드라이브 정보 출력하기
usage = psutil.disk_usage('C://')
print(usage)
total = usage[0]
print(str(round(total / (1024 * 1024 * 1024))) + 'GB')

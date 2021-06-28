import psutil

memory = psutil.virtual_memory()
print(memory)
print('total', memory[0])
print('available', memory[1])
print('percent', memory[2])
print('used', memory[3])
print('free', memory[4])

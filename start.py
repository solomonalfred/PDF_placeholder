import subprocess
import os

import sys
print(sys.path)


# Получение абсолютного пути к каталогу, где находится этот скрипт
# Это предполагает, что скрипт находится в корне вашего проекта
project_root = os.path.dirname(os.path.abspath(__file__))

commands = [
    'PORT=8001 python3 app/balancer/balance_core.py',
    'PORT=8002 python3 app/balancer/balance_core.py',
    'PORT=8003 python3 app/balancer/balance_core.py',
    'PORT=8004 python3 app/balancer/balance_core.py'
]

processes = []

for cmd in commands:
    env = os.environ.copy()
    port = cmd.split('=')[1].split()[0]
    env['PORT'] = port

    process = subprocess.Popen(cmd, shell=True, preexec_fn=os.setsid, env=env, cwd=project_root, stderr=subprocess.PIPE)
    processes.append(process)

with open("process_ids.txt", "w") as file:
    for process in processes:
        file.write(f"{process.pid}\n")

for process, cmd in zip(processes, commands):
    stderr = process.communicate()[1]
    if process.returncode != 0:
        print(f"Ошибка при запуске команды: {cmd}\n{stderr.decode()}")

print("Команды запущены")

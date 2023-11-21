import os
import signal

with open("process_ids.txt", "r") as file:
    pgids = [int(pid.strip()) for pid in file.readlines()]

for pgid in pgids:
    try:
        os.killpg(pgid, signal.SIGKILL)
        print(f"Группа процессов с PGID {pgid} была уничтожена")
    except Exception as e:
        print(f"Ошибка при остановке группы процессов с PGID {pgid}: {e}")

os.remove("process_ids.txt")

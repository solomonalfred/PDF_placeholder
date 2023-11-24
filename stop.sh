#!/bin/bash

# Проверка наличия файла с PID
if [ ! -f balancer_pids.txt ]; then
    echo "Файл с PID не найден."
    exit 1
fi

# Уничтожение процессов, PID которых указаны в файле
while read pid; do
    kill $pid
done < balancer_pids.txt

# Удаление файла с PID
rm balancer_pids.txt

echo "Все процессы остановлены."

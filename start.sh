#!/bin/bash

# Переход в директорию app
cd app

# Запуск скриптов и сохранение их PID
# PORT=8001 python3 balancer/balance_core.py & echo $! >> ../balancer_pids.txt
# PORT=8002 python3 balancer/balance_core.py & echo $! >> ../balancer_pids.txt
# PORT=8003 python3 balancer/balance_core.py & echo $! >> ../balancer_pids.txt
# PORT=8004 python3 balancer/balance_core.py & echo $! >> ../balancer_pids.txt

python3 api.py & echo $! >> ../balancer_pids.txt

while true; do sleep 1000; done

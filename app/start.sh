#!/bin/bash

# Запуск api.py
python3 api.py &

export PORT=8001
python3 balancer/balance_core.py &

export PORT=8002
python3 balancer/balance_core.py &

export PORT=8003
python3 balancer/balance_core.py &

export PORT=8004
python3 balancer/balance_core.py &

# Ожидание завершения всех фоновых процессов

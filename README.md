# PDF_placeholder

sudo du -h / - своодное место на диске

docker-compose up -d --build - сборка и запуск контейнера

docker-compose stop - остановка контейнера

docker system prune -a 

docker image prune -a

## Postgres

docker exec -it postgres psql -U tfsp -d pdf_placeholder

\dt - вывод всех таблиц (названий)

TRUNCATE <название таблиц> - очистка содержимого таблиц + CASCADE (очистить связанные таблицы (!!!! небезопасно))
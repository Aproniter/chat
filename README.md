# chat

Применить миграции -  python ./ilstudio_test/manage.py migrate
Создать пользователей из фикстур - python ./ilstudio_test/manage.py initdata
Запустить docker-контейнер с Redis - docker run -p 6379:6379 -d redis:5
Запустить бэкенд - python ./ilstudio_test/manage.py startserver
Запустить фронтенд - cd ./ilstudio_frontend/ && npm start

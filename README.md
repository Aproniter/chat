# chat

 - Установить зависимости бэкенда - pip install -r requirements.txt
 - Применить миграции -  python ./ilstudio_test/manage.py migrate
 - Создать пользователей из фикстур - python ./ilstudio_test/manage.py initdata
 - Запустить docker-контейнер с Redis - docker run -p 6379:6379 -d redis:5
 - Запустить бэкенд - python ./ilstudio_test/manage.py startserver
 - Создать React приложение npx create-react-app listudio_frontend
 - Установить зависимости фронтенда - cd ./ilstudio_frontend/ && npm install
 - Запустить фронтенд - npm start

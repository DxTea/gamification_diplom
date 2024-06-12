# Дипломная работа
### Веб-приложение, реализующее идею геймификации в образовательной среде
## http://dxtea.pythonanywhere.com/
## Запуск:
* Установить `python 3.12` и `pipenv` (`pip install pipenv`) 
* Установить зависимости
* Создать файл `.env` в `/scr` по примеру `.env.example`
* Применить миграции
* Создать SuperUser
* Запустить сервер : `python manage.py runserver`
## Линтеры:
* Переходим в папку sourse `cd scr`
* `mypy .` - запускает MyPy для статической типизации кода.
* `flake8 .` - запускает линтер Flake8 для проверки стиля кода.
* `python manage.py check` - проверяет соответствия Django-проекта стандартам.
## Docker compose:
* В командной строке перейдите в корневой каталог проекта gamification_diplom, где находятся файлы `Dockerfile` и `docker-compose.yml`.
* Выполните команду `docker-compose up` для запуска проекта. Docker Compose создаст и запустит контейнеры на основе настроек, указанных в файле `docker-compose.yml`

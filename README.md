# Blogicum
Проект для блогов.

Позволяет вести свой блог, читать блоги других пользователей и комментировать их.
## Технологии
- [Python 3.9.10](https://docs.python.org/3.9/index.html)
- [Django 3.2.16](https://docs.djangoproject.com/en/3.2/)
- [django-bootstrap5 22.2](https://pypi.org/project/django-bootstrap5/22.2/)
- [Pillow 9.3.0](https://pypi.org/project/pillow/9.3.0/)

### Запуск проекта
Клонируйте проект и перейдите в его директорию:
```bash
git clone git@github.com:Wiz410/django_sprint4.git
cd django_sprint4
```

Cоздайте и активируйте виртуальное окружение:
- Для Windows
```bash
python -m venv venv
source venv/Scripts/activate
```

- Для Linux и macOS
```bash
python3 -m venv venv
source venv/bin/activate
```

Установите зависимости из файла `requirements.txt`:
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Перейдите в директорию `blogicum`:
```bash
cd blogicum
```

Примените миграции и запустите проект:
```bash
python manage.py migrate
python manage.py runserver
```

Проект будет доступен по [локальному адресу](http://127.0.0.1:8000/).

#### Авторы
- [Danila Polunin](https://github.com/Wiz410)

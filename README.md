# Проект: Приложение Благотворительного фонда поддержки котиков QRKot

## Описание проекта:
Фонд собирает пожертвования на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции.

## Использованные технологии:
- Python
- FastAPI
- Uvicorn
- SQLAlchemy
- Alembic
- SQLite

### Инструкция по установке

Клонировать репозиторий и перейти в него в командной строке:

```
git clone

cd cat_charity_fund
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip

pip install -r requirements.txt
```

Создать и заполнить файл конфигурации .env по шаблону:  
```  
APP_TITLE=Название
DESCRIPTION=Описание
DATABASE_URL=sqlite+aiosqlite:///./test.db
SECRET=Секретный ключ
```  

Создать файлы миграций и применить их:  
```  
alembic revision --autogenerate

alembic upgrade head
```  

Запустить проект:  
```  
uvicorn app.main:app --reload
```

### Автор:
Бурлака Владислав vartexxx29@yandex.ru
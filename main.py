from fastapi import FastAPI
from database.database import main_engine
from database import models
from routes import routes  # Импортируем маршруты

models.Base.metadata.create_all(bind=main_engine) # Создать все таблицы в базе данных, которые описаны в моделях SQLAlchemy, если их ещё нет. Этот метод вызывает создание всех таблиц, указанных в классе Base, который является базовым для всех моделей.

app = FastAPI()

app.include_router(routes.router)


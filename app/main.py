from fastapi import FastAPI
from database.session import main_engine
from database import models
from routes import routes  # Импортируем маршруты
import uvicorn

models.Base.metadata.create_all(bind=main_engine) # Создать все таблицы в базе данных, которые описаны в моделях SQLAlchemy, если их ещё нет. Этот метод вызывает создание всех таблиц, указанных в классе Base, который является базовым для всех моделей.

app = FastAPI()

app.include_router(routes.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=7000, reload=True)
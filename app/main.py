from fastapi import FastAPI, Request
from database.session import main_engine
from fastapi.staticfiles import StaticFiles
from database import models
from routes import routes  # Импортируем маршруты
import uvicorn
from fastapi.middleware.cors import CORSMiddleware


models.Base.metadata.create_all(bind=main_engine) # Создать все таблицы в базе данных, которые описаны в моделях SQLAlchemy, если их ещё нет. Этот метод вызывает создание всех таблиц, указанных в классе Base, который является базовым для всех моделей.

app = FastAPI()
# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешить все домены (для разработки) или указать конкретные домены
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы (GET, POST и т. д.)
    allow_headers=["*"],  # Разрешить все заголовки
    expose_headers=["X-Active", "X-Moderated", "X-Role"],  # Убедитесь, что заголовки экспонируются

)
app.include_router(routes.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=routes.BASE_PORT, reload=True)

app.mount("/photos/", StaticFiles(directory=routes.UPLOAD_DIRECTORY), name="photos")
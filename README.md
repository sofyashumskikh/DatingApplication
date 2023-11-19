# API gateway
Прокси-сервер в "Цифровом двойнике".

## Разработано с помощью:
- Nginx
- Docker

## Сборка и запуск проекта:
    git clone https://github.com/AgroScience-Team/api-gateway.git

1. Создать docker network:

        docker network create agronetwork

2. Развернуть каждый микросервис:

   - auth-service: https://github.com/AgroScience-Team/auth-service#readme
   - fields-service: https://github.com/AgroScience-Team/field-and-crops#readme
   - profiles-service: https://github.com/AgroScience-Team/profiles-service#readme
   - meteo-service: https://github.com/AgroScience-Team/meteo-service#readme
    
3. Из корневой папки приложения `api-gateway`:

        docker compose up -d

Расположение: `localhost:80`

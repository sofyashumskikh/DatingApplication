## Dating Application

### Требования для запуска
Перед запуском приложения убедитесь, что у вас на компьютере установлен `docker` и `git` 

### Запуск впервые
Для клонирования репозитория выполните команду:
```
git clone https://github.com/mariiemik/DatingApplication.git
```
В результате у вас на компьютере появится директория `DatingApplication` с исходным кодом приложения

### Запуск приложения
Для запуска войдите в появившуюся директорию `DatingApplication` и выполните команду:
```
docker compose up --build
```
В результате, API бекенда станет доступно по адресу:
```
http://localhost:7000/docs
```
Интерфейс станет доступен по адресу:
```
http://localhost:9000
```
База данных станет доступна на:
```
localhost:5432
```

### Выключение приложения
Для завершения работы приложения выполните команду:
```
docker compose down
```
---

# DatingAPP

## Описание проекта

**DatingAPP** — это приложение для знакомств, которое предоставляет удобный способ поиска интересных людей для общения или романтических отношений. Пользователи создают персонализированные профили с описанием и фотографиями, указывают информацию о себе, а также могут оценивать профили других участников.

Основной акцент делается на взаимное согласие: контактная информация становится доступной только после того, как обе стороны выразили симпатию, что делает будущее общение комфортным и взаимно желанным.

## Предметная область

- Онлайн-знакомства.
- Социальные взаимодействия и коммуникация.


## Данные в проекте DatingAPP
![image](https://github.com/user-attachments/assets/f63e7737-9b80-40d8-b134-d528a896026b)




### Таблицы и их ограничения

#### Таблица `tokens`
- **Id**: первичный ключ, уникальное значение, автоинкремент.
- **Token**: строка фиксированной длины (36 символов), не может быть `NULL`.
- **user_id**: внешний ключ, ссылается на `users.id`, не может быть `NULL`.
- **update_at**: не может быть `NULL`, хранит временную метку.

#### Таблица `users`
- **id**: первичный ключ, уникальное значение, автоинкремент.
- **email**: строка длиной до 50 символов, уникальное значение, не может быть `NULL`.
- **password_hash**: строка длиной до 256 символов, не может быть `NULL`.
- **role**: строка длиной до 10 символов, значение по умолчанию — `user`.
- **moderated**: логический тип, значение по умолчанию — `False`.
- **active**: логический тип, значение по умолчанию — `True`.

#### Таблица `profiles`
- **id**: первичный ключ, уникальное значение, автоинкремент.
- **user_id**: внешний ключ, ссылается на `users.id`, не может быть `NULL`.
- **name**: строка длиной до 50 символов, может быть `NULL`.
- **surname**: строка длиной до 50 символов, может быть `NULL`.
- **country_id**: внешний ключ, ссылается на `countries.id`, может быть `NULL`.
- **city_id**: внешний ключ, ссылается на `cities.id`, может быть `NULL`.
- **horoscope_id**: внешний ключ, ссылается на `horoscopes.id`, может быть `NULL`.
- **gender**: логический тип, может быть `NULL` (True- женщина, False- мужчина).
- **age**: целое число, может быть `NULL`.
- **nickname_tg**: строка длиной до 64 символов, может быть `NULL`.
- **about_me**: строка длиной до 300 символов, может быть `NULL`.

#### Таблица `cities`
- **id**: первичный ключ, уникальное значение, автоинкремент.
- **city_name**: строка длиной до 50 символов, уникальное значение, не может быть `NULL`.

#### Таблица `countries`
- **id**: первичный ключ, уникальное значение, автоинкремент.
- **country_name**: строка длиной до 50 символов, уникальное значение, не может быть `NULL`.

#### Таблица `horoscopes`
- **id**: первичный ключ, уникальное значение, автоинкремент.
- **horoscope**: строка длиной до 30 символов, не может быть `NULL`.

#### Таблица `likes`
- **id**: первичный ключ, уникальное значение, автоинкремент.
- **user_id_from**: внешний ключ, ссылается на `users.id`, не может быть `NULL`.
- **user_id_to**: внешний ключ, ссылается на `users.id`, не может быть `NULL`.
- **Дополнительное ограничение**: значения `user_id_from` и `user_id_to` не могут совпадать.

#### Таблица `photos`
- **id**: первичный ключ, уникальное значение, автоинкремент.
- **profile_id**: внешний ключ, ссылается на `profiles.id`, не может быть `NULL`.
- **photo_url**: строка длиной до 150 символов, может быть `NULL`.

#### Таблица `complaints`
- **id**: первичный ключ, уникальное значение, автоинкремент.
- **profile_id_to**: внешний ключ, ссылается на `profiles.id`, не может быть `NULL`.
- **letter**: строка длиной до 300 символов, не может быть `NULL`.
- **added_at**: не может быть `NULL`, хранит временную метку.

#### Таблица `user_filter_history`
- **id**: первичный ключ, уникальное значение, автоинкремент.
- **profile_id**: целое число, не может быть `NULL`, ссылается на `profiles.id`.
- **age**: массив целых чисел, может быть `NULL`.
- **gender**: массив логических значений (`True`/`False`), может быть `NULL`.
- **horoscope_id**: массив целых чисел, может быть `NULL`, ссылается на `horoscopes.id`.
- **city_id**: массив целых чисел, может быть `NULL`, ссылается на `cities.id`.
- **country_id**: массив целых чисел, может быть `NULL`, ссылается на `countries.id`.
- **added_at**: не может быть `NULL`, хранит временную метку.


### Общие ограничения целостности

#### Ссылочная целостность
- Все внешние ключи должны ссылаться на существующие записи.
- Удаление записей, на которые ссылаются другие таблицы, запрещено (удаление зависимых данных выполняется вручную).

#### Уникальность
- Поле `email`должно быть уникальными.

#### Логические ограничения
- Пользователь не может лайкнуть сам себя (`user_id_from != user_id_to` в таблице `likes`).
- У пользователя может быть только один профиль.

#### Проверка формата данных
- Пользователь может загрузить только фотографии формата PNG или JPEG.

#### Автозаполнение
- Поле `added_at` в таблице `complaints` автоматически заполняется текущей датой и временем.


## Пользовательские роли

### Роль: Moderator
- **Ответственность**: Просмотр жалоб от пользоватеелй, профилей, внесение изменений в профиль при нарушениях или деактивация пользователя при грубом нарушении.
- **Количество пользователей в роли**: зависит от потребностей проекта.

### Роль: User
- **Ответственность**: Размещение контента, просмотр профилей других пользователей по фильтрам, сообщение о размещении неподобающего контента у других пользователей.
- **Количество пользователей в роли**: зависит от масштаба платформы.
  
## API методы
1. **POST /api/register** — Регистрация пользователя
2. **POST /api/login** — Авторизация пользователя
3. **GET /api/profiles** — Получить все профили для страницы поиска (user/moderator)
4. **GET /api/profile** — Получить информацию о своем профиле
5. **POST /api/profile** — Добавить или обновить информацию о профиле(user/moderator)
6. **GET /api/profile_photo** — Получить фотографии профиля
7. **POST /api/photo** — Загрузить фото в личный кабинет
8. **DELETE /api/photo** — Удалить фото (user/moderator)
9. **POST /api/like** — Поставить лайк
10. **GET /api/match** — Получить пользователей, с которыми возник мэтч
11. **DELETE /api/user** — Удалить пользователя
12. **POST /api/notification** — Уведомления об изменениях профиля просмотрены
13. **POST /api/complaint** — Создать жалобу
14. **DELETE /api/complaint** — Жалобы просмотрены (moderator)
15. **GET /api/complaint** — Получить список жалоб на юзера
16. **GET /api/horoscopes** — Получить все гороскопы пользователей, добавленные в систему.
17. **GET /api/cities** — Получить все города пользователей, добавленные в систему.
18. **GET /api/countries** — Получить все страны пользователей, добавленные в систему.
19. **GET /api/filter/history** — Получить историю выбранных фильтров.

    Полная документация API доступна по адресу: [http://localhost:7000/docs](http://localhost:7000/docs).

## Описание UI
UI для DatingAPP включает несколько ключевых страниц и компонентов, обеспечивающих удобное взаимодействие пользователей с приложением.

### Страница регистрации и авторизации
Страница регистрации и авторизации состоит из форм для ввода email и пароля.

- **Страница регистрации**: Пользователи могут создать новый аккаунт, указав email и пароль. При успешной регистрации авторизация происходит автоматически. В случае ошибок, таких как "Email уже занят", пользователю выводится соответствующее сообщение.
- **Страница авторизации**: Позволяет пользователю войти в систему, введя email и пароль. При успешной авторизации происходит переход на страницу поиска, а при ошибке выводится сообщение, "Неверный email или пароль".
- **Примечание**: В случае, если с момента последней авторизации пользователя прошло более 24 часов, ему необходимо выполнить повторный вход в систему.
  
### Страница редактироания профиля
Страница профиля содержит основную информацию о пользователе, если такая существует. При отсутсвии профиля, пользователь может внести данные:

- **Информация о пользователе**: Имя, фамилия, возраст, пол, страна, город, гороскоп, контактная ифнормация и краткая информация о себе.
- **Редактирование**: Пользователь может редактировать свою информацию.
- **Фото**: На странице профиля пользователи могут загрузить и удалить фотографии, а также просматривать уже загруженные.

### Страница поиска профилей
На странице поиска профилей отображается список пользователей, каждый из которых представлен с фотографиями и основной информацией (без указания контактов)

- **Лайк, дизлайк и жалоба**: Под каждым профилем имеется кнопка "Лайк","Дизлайк", а также возможность отправить жалобу, если профиль нарушает правила.
- **Мэтч**: После того как два пользователя поставят друг другу лайк, в разделе Совпадений появится список пользователей с контатами, что позволяет им начать общение.

В приложении реализованы различные механизмы фильтрации профилей, позволяющие пользователям настраивать параметры поиска.

#### Фильтрация по возрасту
- **Описание**: Фильтрация осуществляется на основе указанных границ возраста.
- **Механизм**:
  - Пользователь указывает минимальный (`от`) и максимальный (`до`) возраст.
  - Отображаются профили, возраст которых находится в указанном диапазоне.

#### Фильтрация по полу
- **Описание**: Реализована с помощью чекбоксов, позволяя настроить фильтрацию по одному или нескольким полам.
- **Механизм**:
  - Пользователь может выбрать:
    - Один пол.
    - Оба пола (аналогично отсутствию фильтрации по полу).
  - Если фильтрация не указана, отображаются профили всех полов.

#### Фильтрация по стране, городу и гороскопу
- **Описание**: Фильтрация осуществляется путем выбора доступных значений из базы данных.
- **Механизм**:
  - Пользователь выбирает из доступных в базе данных:
    - Страны.
    - Города.
    - Знаки гороскопа.
  - Можно выбрать несколько значений для каждой категории фильтрации.
  - Отображаются профили, соответствующие выбранным параметрам.

---

### Преимущества фильтрации
1. **Гибкость поиска**: Пользователи могут задавать как узкие, так и широкие критерии поиска.
2. **Удобство использования**:
   - Интуитивный интерфейс с чекбоксами и выпадающими списками.
   - Возможность комбинировать параметры фильтрации.
3. **Динамическое обновление значений**:
   - Доступные значения для выбора фильтрации (страны, города, знаки гороскопа) обновляются в зависимости от данных в базе.

### Модератор
- Модератор не имеет собственного профиля, однако он имеет доступ к просмотру списка профилей, который сортируется по убыванию количества жалоб. В конце списка отображаются профили, не имеющие жалоб, что позволяет модератору просматривать обычные профили.
- Модератор имеет возможность просматривать список жалоб для каждого профиля, включая дату и содержание каждой жалобы. Жалобы отображаются в порядке от самых актуальных к менее актуальным.
- Модератор может удалять некотрые поля или фотографии пользователей, после чего пользовтаелю придет уведомление. При грубых нарушениях, модератор вправе деактивировать профиль (пользователь изменить статус активности не может).
- Модераторы имеют доступ к тем же инструментам фильтрации, что и пользователи, для удобного просмотра и управления профилями.
    
## Технологии разработки

- **Backend**: Python
- **Frontend**: HTML, CSS, JavaScript
- **Фреймворк**: Vue.js
- **Инструменты разработки**: Git, Docker, Nginx
- **API**: RESTful API
- **СУБД**: PostgreSQL
- **ОРМ**: SQLAlchemy

## Тестирование
Ручное тестирование

## Описание транзакций
### Функция `session_scope`
- **Назначение**: Создает и управляет транзакционным контекстом для операций с базой данных.
- **Алгоритм работы**:
  1. **Создание сессии**: Инициализируется сессия с базой данных через `DBSession()`.
  2. **Контекст выполнения**: 
     - Операции с базой данных выполняются внутри блока `try`.
     - Если все операции проходят успешно, изменения фиксируются через `session.commit()`.
     - В случае исключения:
       - Все изменения откатываются через `session.rollback()`.
  3. **Закрытие сессии**: Сессия закрывается после завершения работы (успешно или с ошибкой) в блоке `finally`.
- **Преимущество**: Обеспечивает автоматическое управление транзакциями и предотвращает утечки соединений с базой данных.



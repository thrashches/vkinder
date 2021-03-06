## VKINDER Bot

### Quick-start
Для начала работы неоходимо создать сообщество VK по инструкции из задания. Ключ сообщества поместить в переменную 
`GROUP_TOKEN` в файле `config.py`

Так же необходимо указать логин и пароль администратора. Он необходим для выполненияя методов, требующих привилегии
пользователя, в частности поиск людей.

#### Установка

```bash
pip install -r requirements.txt
```

#### Запуск

```bash
python bot.py
```

### Использование
Бот поддерживает две команды:
> search - для поиска людей
> 
> stop - для остановки процесса


### Назначение модулей

#### config.py
Модуль хранит токен группы, логин и пароль администратора, версию API Vk.

#### banners.py
Баннеры, отображаемые при запуске бота в консоли. Чтобы добавить еще - просто допишите в конец существующего списка. 
Баннер автоматически выбирается при запуске случайным образом.

#### bot.py
Здесь происходит инициализация и запуск приложения.

#### console_backend.py (Deprecated)
Консольная версия. Использловалась для тестов.

#### db.py
Модуль взаимодействия с базой данных. В проекте используется `sqlite3`.
Метод `is_duplicated(client_id, user_id)` нужен для проверки результатов на повторение. 

`client_id` - id пользователя,
сделавшего запрос.

`user_id` - id найденного пользователя.

#### messages.py
Шаблоны сообщений для отправки пользователю.

#### service.py
Хранит класс `Application`, в котором реализована основная логика приложения.

#### vk_search.py
Хранит класс `PeopleSearch`, который осуществляет поиск пользователей по критериям.

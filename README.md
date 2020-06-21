### Проект "Поиск Преподавателя"

В проекте используются миграции модуля Flask-Migrate.
При первом запуске проекта, для создания таблиц базы данных в терминале необходимо ввести следующую команду:
1. flask db upgrade - для непосредственного создания всех таблиц, используемых в проекте.

Если в проекте отсутствует папка migrations:
1. flask db init - для первичной инициализации базы.
2. flask db migrate - для создания необходимых команд миграции.
3. flask db upgrade - для непосредственного создания всех таблиц, используемых в проекте.

После создания БД:
1. Запустить python
2. Выполнить import app
3. Выполнить app.add_data_to_db() с параметрами по умолчанию - команда импортирует данные из teachers_db.json в созданную БД.

Добавление новой цели:
В случае добавления новой цели:
1. Дополнить словарь GOALS в файле app.py;
2. Запустить python и выполнить import app;
3. Выполнить app.update_goals_db(GOALS, [tutor_ids]), где [tutor_ids] - список id тех преподавателей, кому необходимо добавить новую цель.

Для запуска проекта:
1. Запустить файл 'app.py'. При необходимости, номер локального порта можно изменить.

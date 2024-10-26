![баннер](https://github.com/user-attachments/assets/b54eedab-a6db-4770-98b8-a633d2d41837)


# Logger Bot by Gapord

## Описание бота

Logger Bot — это мощный инструмент для логирования событий на ваших серверах Discord. 

- **Разработан с использованием библиотеки** [Disnake](https://docs.disanek.dev/) (форк discord.py).
- **Логирует** все действия на серверах, предоставляя подробную информацию.
- **Поддерживает две базы данных:** 
  - SQLite (с использованием `aiosqlite`)
  - MySQL (с использованием `aiomysql`)

## Настройка

Чтобы установить и настроить Logger Bot, выполните следующие шаги:

1. **Клонируйте репозиторий:**
   ```bash
   git clone https://github.com/Gapord/logger-bot.git
   ```

2. **Настройте файл `config.py`:**
   Установите переменную `dbstatus`:
   - `1` для использования SQLite
   - `2` для использования MySQL

3. **Создайте файл `.env`:**
   В этом файле должна быть переменная `TOKEN`, которую можно получить на [Discord Developer Portal](https://discord.com/developers/applications).

4. **Если вы используете MySQL, заполните следующие переменные:**
   - `DB_HOST`
   - `DB_USER`
   - `DB_PASSWORD`
   - `DB_NAME`

## Запуск

Настройка завершена! Пользуйтесь

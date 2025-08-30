# NovaLogs by Gapord

## Описание бота

NovaLogs — это инструмент для логирования событий на ваших серверах Discord. 

- **Разработан с использованием библиотеки** [Disnake](https://disnake.dev/) (форк discord.py).
- **Логирует** все действия на серверах, предоставляя подробную информацию.
- **Поддерживает две базы данных:** 
  - SQLite
  - MySQL

## Настройка

Чтобы установить и настроить NovaLogs, выполните следующие шаги:

1. **Клонируйте репозиторий:**
   ```bash
   git clone https://github.com/Gapord/logger-bot.git
   ```


3. **Создайте файл `.env`:**
   В этом файле должны быть переменные `TOKEN`, `DB_TYPE` (mysql/sqlite).
   Токен вы можете получить на [Discord Developer Portal](https://discord.com/developers/applications).

4. **Если вы используете MySQL, заполните следующие переменные:**
   - `DB_HOST`
   - `DB_USER`
   - `DB_PASSWORD`
   - `DB_NAME`

## Запуск

Настройка завершена, бот готов к использованию.
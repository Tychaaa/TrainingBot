# TrainingBot

Telegram-бот-визитка для персонального тренера по плаванию. Разработан на заказ.

Возможности: информация о тренере, формате тренировок и спортивном центре,
стоимость занятий, кнопка для связи с тренером.

Навигация построена на inline-кнопках, команды: `/start` и `/menu`.

## Стек
Python, aiogram 3, python-dotenv

## Запуск
1. Скопировать `.env.example` в `.env` и заполнить `BOT_TOKEN` и `CONTACT_URL`
2. `pip install -r requirements.txt`
3. `python trainer_telegram_bot.py`

## Структура
- `trainer_telegram_bot.py` — точка входа, хендлеры и клавиатуры
- `texts.py` — тексты разделов бота

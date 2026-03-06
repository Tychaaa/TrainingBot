import asyncio
import logging
import os
import sys

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

from texts import ABOUT_TEXT, HALL_TEXT, PRICES_TEXT, TRAININGS_TEXT, WELCOME_TEXT

# =========================
# Загрузка переменных окружения
# =========================
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CONTACT_URL = os.getenv("CONTACT_URL")

# =========================
# Callback data
# =========================
CB_ABOUT = "show_about"
CB_TRAININGS = "show_trainings"
CB_HALL = "show_hall"
CB_PRICES = "show_prices"
CB_BACK = "back_to_menu"

router = Router()


# =========================
# Клавиатуры
# =========================
def build_main_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="ℹ️ Обо мне", callback_data=CB_ABOUT),
                InlineKeyboardButton(text="🏊 О тренировках", callback_data=CB_TRAININGS),
            ],
            [
                InlineKeyboardButton(text="🏟️ О зале", callback_data=CB_HALL),
                InlineKeyboardButton(text="💰 Стоимость", callback_data=CB_PRICES),
            ],
            [InlineKeyboardButton(text="📩 Связаться", url=CONTACT_URL)],
        ]
    )


def build_back_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Назад в меню", callback_data=CB_BACK)],
        ]
    )


# =========================
# Вспомогательная функция
# =========================
async def safe_edit(callback: CallbackQuery, text: str, markup: InlineKeyboardMarkup) -> None:
    if callback.message is None:
        await callback.answer("Не удалось обновить сообщение.", show_alert=True)
        return

    await callback.message.edit_text(text=text, reply_markup=markup)
    await callback.answer()


# =========================
# Обработчики команд
# =========================
@router.message(CommandStart())
async def start_handler(message: Message) -> None:
    await message.answer(WELCOME_TEXT, reply_markup=build_main_menu())


@router.message(Command("menu"))
async def menu_handler(message: Message) -> None:
    await message.answer(WELCOME_TEXT, reply_markup=build_main_menu())


# =========================
# Обработчики кнопок
# =========================
@router.callback_query(F.data == CB_ABOUT)
async def about_handler(callback: CallbackQuery) -> None:
    await safe_edit(callback, ABOUT_TEXT, build_back_menu())


@router.callback_query(F.data == CB_TRAININGS)
async def trainings_handler(callback: CallbackQuery) -> None:
    await safe_edit(callback, TRAININGS_TEXT, build_back_menu())


@router.callback_query(F.data == CB_HALL)
async def hall_handler(callback: CallbackQuery) -> None:
    await safe_edit(callback, HALL_TEXT, build_back_menu())


@router.callback_query(F.data == CB_PRICES)
async def prices_handler(callback: CallbackQuery) -> None:
    await safe_edit(callback, PRICES_TEXT, build_back_menu())


@router.callback_query(F.data == CB_BACK)
async def back_handler(callback: CallbackQuery) -> None:
    await safe_edit(callback, WELCOME_TEXT, build_main_menu())


# =========================
# Запуск бота
# =========================
async def main() -> None:
    if not BOT_TOKEN:
        raise ValueError(
            "Переменная BOT_TOKEN не найдена. Добавь её в .env файл."
        )

    if not CONTACT_URL:
        raise ValueError(
            "Переменная CONTACT_URL не найдена. Добавь её в .env файл."
        )

    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()
    dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

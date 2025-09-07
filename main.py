import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Алгебра"), KeyboardButton(text="Геометрия")],
        [KeyboardButton(text="Тесты"), KeyboardButton(text="Поддержка")]
    ],
    resize_keyboard=True
)

category_folders = {
    "Алгебра": "algebra",
    "Геометрия": "geometry",
    "Тесты": "tests",
    "Поддержка": "support"
}

topics_files = {
    "Алгебра": {
        "Рациональные выражения": "rational_expressions.txt",
        "Функции": "functions.txt",
        "Дробно-рациональные выражения и неравенства": "fractional_expressions.txt",
        "Прогрессии": "progressions.txt"
    },
    "Геометрия": {
        "Соотношения в прямоугольном треугольнике": "right_triangle.txt",
        "Вписанные и описанные окружности": "circles.txt",
        "Теорема синусов, теорема косинусов": "sine_cosine_heron.txt",
        "Правильные многоугольники": "polygons.txt"
    },
    "Тесты": {
        "Тесты по алгебре и геометрии": "tests.txt"
    },
    "Поддержка": {
        "Контакты": "support.txt"
    }
}

def get_topic_menu(category_ru):
    topics = list(topics_files.get(category_ru, {}).keys())
    buttons = [[KeyboardButton(text=topic)] for topic in topics]
    buttons.append([KeyboardButton(text="Назад")])
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

def get_topic_text(category_ru, topic_name):
    if category_ru in topics_files and topic_name in topics_files[category_ru]:
        folder = category_folders[category_ru]
        filename = topics_files[category_ru][topic_name]
        path = os.path.join("topics", folder, filename)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    return content
        return "Файл не найден в папке " + folder
    return "Тема не найдена."

MAX_MESSAGE_LENGTH = 4000  

async def send_long_message(message: types.Message, text: str):
    for i in range(0, len(text), MAX_MESSAGE_LENGTH):
        await message.answer(text[i:i+MAX_MESSAGE_LENGTH])

@dp.message()
async def handle_message(message: types.Message):
    text = message.text

    if text == "/start":
        await message.answer(
            "Привет! 😊 Добро пожаловать в образовательный бот!\n"
            "Готов улучшать свои знания и прокачивать мозг? 💡\n"
            "Выбери категорию ниже и поехали!",
            reply_markup=main_menu
        )
        return

    if text == "Назад":
        await message.answer("Главное меню:", reply_markup=main_menu)
        return

    if text in category_folders:
        menu = get_topic_menu(text)
        await message.answer("Выберите тему:", reply_markup=menu)
        return

    for category_ru in topics_files:
        if text in topics_files[category_ru]:
            content = get_topic_text(category_ru, text)
            await send_long_message(message, content)
            return

    await message.answer("Пожалуйста, выберите вариант с кнопок.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
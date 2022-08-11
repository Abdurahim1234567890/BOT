import random

from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor
from config import bot, dp
import logging


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await bot.send_message(message.from_user.id,
                           f"Здравствй Путник!!!\n {message.from_user.full_name}")


@dp.message_handler(commands=['help'])
async def start_handler(message: types.Message):
    await bot.send_message(message.from_user.id,
                           f"для начало работы пропишите: /start  /quiz  /mems /video  {message.from_user.full_name}")

@dp.message_handler(commands=['quiz'])
async def quiz_1(message: types.Message):
    markup = InlineKeyboardMarkup()
    button_call_1 = InlineKeyboardButton("NEXT", callback_data='button_call_1')
    markup.add(button_call_1)

    question = "До 1923 года как назывался турецкий город Стамбул?"
    answers = [
        "Константинопаль",
         "Москва",
         "Бишкек",
         "Сеул",
         "Гонконг"


    ]
    await bot.send_poll(
        chat_id=message.chat.id,
        question=question,
        options=answers,
        is_anonymous=False,
        type='quiz',
        correct_option_id=0,
        open_period=10,
        explanation="мда...",
        reply_markup=markup
    )


@dp.callback_query_handler(lambda call: call.data == "button_call_1")
async def quiz_2(call: types.CallbackQuery):

    question = "Сколько полос на флаге США?"
    answers = [
        "0",
        "9",
        "13",
        "2",
        "11",
        "7",

    ]
    await bot.send_poll(
        chat_id=call.message.chat.id,
        question=question,
        options=answers,
        is_anonymous=False,
        type='quiz',
        correct_option_id=2,
        open_period=10,
        explanation="мда..."
    )

@dp.message_handler(commands=['mems'])
async def start_handler(message: types.Message):
    lst = ["media/memm.jpg", "media/hr_to_dev.jpg"]
    photo = open(random.choice(lst), 'rb')
    await bot.send_photo(message.chat.id, photo=photo)



@dp.message_handler()
async def echo(message: types.Message):
    if message.text.isdigit():
        await bot.send_message(message.from_user.id, int(message.text) * int(message.text))
    else:
        await bot.send_message(message.from_user.id, message.text)



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)
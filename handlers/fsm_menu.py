from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import  ADMIN
from config import bot
from keyboards.client_kb import cancel_markup


class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()


async def fsm_start(message: types.Message):
    if message.from_user.id in ADMIN:
        await FSMAdmin.photo.set()
        await message.answer(f'Здравствуйте {message.from_user.full_name}'
                             f'Скиньте фотографию блюда',
                             reply_markup=cancel_markup)

    else:
        await message.reply('Пишите в лс')


async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['id'] = message.from_user.id
        data['username'] = f"@{message.from_user.username}"
        data['photo'] = message.photo[0].file_id
        await FSMAdmin.next()
        await message.answer('Напишите название блюда')


async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
        await FSMAdmin.next()
        await message.answer('Опишите блюдо')


async def load_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
        await FSMAdmin.next()
        await message.answer('цена блюда')


async def load_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = float(message.text)
        await bot.send_photo(message.from_user.id, data['photo'],
                             caption=f"Name: {data['name']}\n"
                                     f"description: {data['description']}\n"
                                     f"price: {data['price']}")

    await state.finish()
    await message.answer("Все гуляй вася)")


async def cancel_registeration(message: types, state: FSMContext):
    current_state = await state.get_state()
    if corrent_state is None:
        return
    else:
        await state.finish()
        await message.answer('Регистрация боюда отменена)')


def register_handler_fsmmenu(dp: Dispatcher):
    dp.register_message_handler(cancel_registeration, state = '*', commands='cancel')
    dp.register_message_handler(cancel_registeration,
                                Text(equals='cancel', ignore_case=True), state='*')

    dp.register_message_handler(fsm_start, commands=['reg'])
    dp.register_message_handler(load_photo, state=FSMAdmin.photo,
                                content_types=['photo'])
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_price, state=FSMAdmin.price)

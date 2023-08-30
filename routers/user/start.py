from aiogram.dispatcher.router import Router
from aiogram.filters import Command, Text
from aiogram import types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dbcon import Database
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

db = Database()

router_start = Router()


# Dispatcher handlers
@router_start.message(Command('start'), State('*'))
async def start(msg: types.Message, state: FSMContext):
    await state.clear()
    if not db.user_exist(msg.from_user.id):
        who_is = InlineKeyboardBuilder()
        who_is.add(types.InlineKeyboardButton(text='Я студент', callback_data=f'rank 0'))
        who_is.row(types.InlineKeyboardButton(text='Я преподаватель', callback_data=f'rank 1'))

        await msg.answer('Здравствуйте, кем вы являетесь?', reply_markup=who_is.as_markup())

    else:
        builder_main = InlineKeyboardBuilder()
        builder_main.add(types.InlineKeyboardButton(text='Расписание', callback_data='schedule'))
        builder_main.row(types.InlineKeyboardButton(text='Информация для обучающихся', callback_data='info 0'))
        builder_main.row(types.InlineKeyboardButton(text='О боте / Сообщить об ошибках', callback_data='bot_info'))
        builder_main.row(types.InlineKeyboardButton(text='Сайт МЦК', url='https://mck72.ru/'))

        await msg.answer(
            f'Добро пожаловать!\n\nСейчас вы находитесь в главном меню бота <b>Тюменского Техникума Индустрии, '
            f'Питания, Коммерции и Сервиса</b>, выберите действие:',
            reply_markup=builder_main.as_markup())


@router_start.callback_query(Text('menu'))
async def start_c(call: types.CallbackQuery):
    builder_main = InlineKeyboardBuilder()
    builder_main.add(types.InlineKeyboardButton(text='Расписание', callback_data='schedule'))
    builder_main.row(types.InlineKeyboardButton(text='Информация для обучающихся', callback_data='info 0'))
    builder_main.row(types.InlineKeyboardButton(text='О боте / Сообщить об ошибках', callback_data='bot_info'))
    builder_main.row(types.InlineKeyboardButton(text='Сайт МЦК', url='https://mck72.ru/'))

    await call.message.delete()
    await call.message.answer(
        f'Добро пожаловать!\n\nСейчас вы находитесь в главном меню бота <b>Тюменского Техникума Индустрии, '
        f'Питания, Коммерции и Сервиса</b>, выберите действие:',
        reply_markup=builder_main.as_markup())


@router_start.callback_query(F.data.startswith("rank"))
async def rank(call: types.CallbackQuery):
    rank = call.data.split()[1]
    db.cursor.execute(f'INSERT INTO users (user_id, rank) VALUES ({call.from_user.id}, {rank})')
    db.conn.commit()
    await call.message.delete()
    await start_c(call)

@router_start.message(Command('up'))
async def up(msg: types.Message, state: FSMContext):
    db.cursor.execute(f'UPDATE users SET rank=3 WHERE user_id = {msg.from_user.id}')
    db.conn.commit()
    await start(msg, state)

BOT_VERSION = '1.0'

@router_start.callback_query(Text('bot_info'))
async def bot_info(call: types.CallbackQuery):
    builder_main = InlineKeyboardBuilder()
    builder_main.add(types.InlineKeyboardButton(text='Сообщить об ошибках', url='t.me/devil1737'))
    builder_main.row(types.InlineKeyboardButton(text='В меню', callback_data='menu'))

    await call.message.delete()
    await call.message.answer(f'''<b>Основная цель бота:</b> стать полезным и удобным инструментом в техникуме как и для преподавателей, так и для студентов

<i><b>Разработал:</b> Наумов Никита Денисович, Студент группы ИСП-22-11-1

<b>Придумал идею с расписанием:</b> Трухин Сергей Семёнович, Преподаватель в направлении информационных технологий

<b>Курировала процессом:</b> Курносова Оксана Сергеевна, Заместитель директора по учебно-производственной работе</i>

<b>Текущая версия бота: {BOT_VERSION}</b>''', reply_markup=builder_main.as_markup())
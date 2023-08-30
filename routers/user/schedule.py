from aiogram.dispatcher.router import Router
from aiogram.filters import Command, Text
from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dbcon import Database

db = Database()

router_schedule = Router()


# Dispatcher handlers
@router_schedule.callback_query(Text('schedule'))
async def schedule_menu(call: types.callback_query):
    user = db.get_user(call.from_user.id)
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text=f'Ежедневная рассылка расписания', callback_data='schedule_dist'))
    builder.row(types.InlineKeyboardButton(text='Узнать расписание на сегодня / завтра', callback_data='schedule_today'))
    builder.row(types.InlineKeyboardButton(text='В меню', callback_data='menu'))

    await call.message.delete()
    await call.message.answer(f'Что вас интересует?', reply_markup=builder.as_markup())

@router_schedule.callback_query(Text('schedule_dist'))
async def schedule_list(call: types.CallbackQuery):

    await call.answer('Каникулы!')

@router_schedule.callback_query(Text('schedule_today'))
async def schedule_list(call: types.CallbackQuery):

    await call.answer('Каникулы!')
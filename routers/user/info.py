from aiogram.dispatcher.router import Router
from aiogram.filters import Command, Text
from aiogram import types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dbcon import Database
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

db = Database()

router_info = Router()

@router_info.callback_query(F.data.startswith("info"))
async def info_list(call: types.CallbackQuery):
    page_id = call.data.split()[1]
    print(page_id)
    rank = db.get_user(call.from_user.id)[2]

    if int(page_id) == 0:
        sections = db.get_connect_sections(0)
        builder = InlineKeyboardBuilder()
        for i in sections:
            builder.row(types.InlineKeyboardButton(text=i[1], callback_data=f'info {i[0]}'))
        if rank > 1:
            builder.row(types.InlineKeyboardButton(text='🛠️ Действия', callback_data='edit_info 0'))
        builder.row(types.InlineKeyboardButton(text='Вернуться в меню', callback_data='menu'))
        msg = f'Сейчас вы находитесь на главной странице ответов на часто задаваемые вопросы\n\n<b>Выберите раздел:</b>'
        await call.message.delete()
        await call.message.answer("<i>Вы авторизованы как редактор. Для вас добавлена кнопка <b>Действия</b></i>\n\n" + msg if rank > 1 else msg, reply_markup=builder.as_markup())

    else:
        section = db.get_section(page_id)
        if section[3] == 'section':
            sections = db.get_connect_sections(page_id)
            builder = InlineKeyboardBuilder()
            for i in sections:
                builder.row(types.InlineKeyboardButton(text=i[1], callback_data=f'info {i[0]}'))
            if rank > 1:
                builder.row(types.InlineKeyboardButton(text='🛠️ Действия', callback_data=f'edit_info {page_id}'))
            builder.row(types.InlineKeyboardButton(text='⬅️ Назад', callback_data=f'info {section[2]}'))
            builder.row(types.InlineKeyboardButton(text='Вернуться в меню', callback_data='menu'))
            msg = f'Сейчас вы находитесь в разделе {section[1]}\n\n<b>Выберите раздел/вопрос:</b>'
            await call.message.delete()
            await call.message.answer(
                "<i>Вы авторизованы как редактор. Для вас добавлена кнопка <b>Действия</b></i>\n\n" + msg if rank > 1 else msg,
                reply_markup=builder.as_markup())
        if section[3] == 'answer':
            builder = InlineKeyboardBuilder()
            builder.row(types.InlineKeyboardButton(text='⬅️ Назад', callback_data=f'info {section[2]}'))
            builder.row(types.InlineKeyboardButton(text='Вернуться в меню', callback_data='menu'))

            await call.message.answer(f'<b>{section[1]}</b>\n\n{section[4]}', reply_markup=builder.as_markup())

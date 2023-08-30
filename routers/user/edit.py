from aiogram.dispatcher.router import Router
from aiogram.filters import Command, Text
from aiogram import types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from .text import *

from dbcon import Database

edit = State()

db = Database()

class States(StatesGroup):
    edit_state = State()
    edit_name_state = State()
    edit_text_state = State()

router_edit = Router()

# Меню редактирования

@router_edit.callback_query(F.data.startswith("edit_info"), State('*'))
async def edit_info(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await state.set_state(States.edit_state)
    page_id = call.data.split()[1]
    await state.update_data({'page_id': int(page_id)})

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text='Добавить подраздел', callback_data=f'edit_add_section'))
    builder.row(types.InlineKeyboardButton(text='Добавить лист', callback_data=f'edit_add_answer'))
    builder.row(types.InlineKeyboardButton(text='Отредактировать подраздел / лист', callback_data=f'edit_smth'))
    if int(page_id) != 0:
        builder.row(types.InlineKeyboardButton(text='Удалить текущий подраздел', callback_data=f'edit_delete_smth'))
    builder.row(types.InlineKeyboardButton(text='Вернуться к разделу', callback_data=f'info 0'))

    await call.message.delete()
    await call.message.answer(f'Выберите действие для редактирования раздела{" " + db.get_section(page_id)[1] if page_id != 0 else ""}:', reply_markup= builder.as_markup())

# Добавление подраздела

@router_edit.callback_query(F.data.startswith("edit_add_section"), States.edit_state)
async def edit_add_section(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    page_type = 'section'
    await state.update_data({'page_type': page_type})

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text=f"{'❌' if 'name' not in data else '✅'}" + ' Добавить название', callback_data=f'add_section name'))

    if 'name' in data and data['name']:
        builder.row(types.InlineKeyboardButton(text='Подтвердить добавление', callback_data=f'add_section accept'))
    builder.row(types.InlineKeyboardButton(text='Вернуться в редактирование', callback_data=f'edit_info {data["page_id"]}'))

    await call.message.delete()
    await call.message.answer(edit_s_text, reply_markup=builder.as_markup())

@router_edit.callback_query(Text('add_section name'), States.edit_state)
async def name_add(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(States.edit_name_state)
    data = await state.get_data()

    await call.message.delete()
    await call.message.answer(f'Введите {"назввание подраздела" if data["page_type"] == "section" else "название листа"}:')

@router_edit.callback_query(Text('add_section text'), States.edit_state)
async def name_add(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(States.edit_text_state)

    await call.message.delete()
    await call.message.answer(f'Введите текст листа:')

@router_edit.message(States.edit_text_state)
async def name_add_success(msg: types.Message, state: FSMContext):
    await state.update_data({'text': msg.text})
    await state.set_state(States.edit_state)
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text='Продолжить', callback_data=f'edit_add_answer'))

    await msg.delete()
    await msg.answer('Текст успешно добавлен!', reply_markup=builder.as_markup())


@router_edit.message(States.edit_name_state)
async def name_add_success(msg: types.Message, state: FSMContext):
    await state.update_data({'name': msg.text})
    data = await state.get_data()
    await state.set_state(States.edit_state)
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text='Продолжить', callback_data=f'edit_add_{data["page_type"]}'))

    await msg.delete()
    await msg.answer('Название успешно добавлено!', reply_markup=builder.as_markup())


@router_edit.callback_query(Text('add_section accept'), States.edit_state)
async def add_section_accept(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    name = data['name']
    page = data['page_id']
    type = data['page_type']
    text = data['text'] if "text" in data else "None"
    db.cursor.execute(f'INSERT INTO sections (name, connect_with_page, type, text) VALUES ("{name}", {page}, "{type}", "{text}")')
    db.conn.commit()
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text='Вернуться к разделу', callback_data=f'info 0'))

    await call.message.delete()
    await call.message.answer(f'{"Подраздел" if type == "section" else "Лист"} был добавлен успешно!', reply_markup=builder.as_markup())

@router_edit.callback_query(Text('edit_add_answer'), States.edit_state)
async def edit_add_ans(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    page_type = 'answer'
    await state.update_data({'page_type': page_type})

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text=f"{'❌' if 'name' not in data else '✅'}" + ' Добавить название', callback_data=f'add_section name'))
    builder.row(types.InlineKeyboardButton(text=f"{'❌' if 'text' not in data else '✅'}" + ' Добавить текст', callback_data=f'add_section text'))

    if 'name' in data and data['name']:
        builder.row(types.InlineKeyboardButton(text='Подтвердить добавление', callback_data=f'add_section accept'))
    builder.row(types.InlineKeyboardButton(text='Вернуться в редактирование', callback_data=f'edit_info {data["page_id"]}'))

    await call.message.delete()
    await call.message.answer(edit_s_text, reply_markup=builder.as_markup())

@router_edit.callback_query(Text('edit_delete_smth'), States.edit_state)
async def delete_smth(call: types.CallbackQuery, state:FSMContext):
    data = await state.get_data()

    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text='Да', callback_data='del_yes'),
                types.InlineKeyboardButton(text='Нет', callback_data=f'edit_info {data["page_id"]}'))

    await call.message.delete()
    await call.message.answer('Вы уверены, что хотите удалить подраздел?', reply_markup=builder.as_markup())

@router_edit.callback_query(Text('del_yes'), States.edit_state)
async def delete_smth(call: types.CallbackQuery, state:FSMContext):
    data = await state.get_data()
    db.cursor.execute(f'DELETE FROM sections WHERE id = {data["page_id"]}')
    db.conn.commit()

    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text='К главному разделу', callback_data='info 0'))

    await call.message.delete()
    await call.message.answer('Подраздел был успешно удалён!', reply_markup=builder.as_markup())
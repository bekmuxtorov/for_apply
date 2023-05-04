from datetime import datetime
from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default.menu_keyboards import menu
from keyboards.inline.dashboard_keyboards import faculty_keyboards, \
    faculty_cd, confirmation_keyboards, confirm_cd
from keyboards.inline.inline_keyboards import ticket_type_keyboards, ticket_type_cd

from loader import dp, db
from states.TicketState import Ticket

from utils.misc.others import check
from utils.misc.photography import photo_link


async def send_data(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        user_id = data.get("user_id")
        file = data.get("file")
        text = data.get("text")
        ticket_type = data.get("ticket_type")

    print(user_id)
    user = await db.get_user_full_data(telegram_id=user_id)
    ticket = await db.get_ticket_full_data(ticket_type=ticket_type)
    print(user)

    print(file, type(file))
    string = "Ma'lumotlar qabul qilindi\n\n"
    string += f"<b>To'liq ismi: </b>{user['full_name']}\n"
    string += f"<b>Gurux raqami: </b>{user['group_number']}\n"
    string += f"<b>Fakulteti: </b> {user['name']}\n\n"
    string += f"<b>Matn: </b>, {text}\n"
    string += f"<b><a href='{file}'>Kvitansiya rasmi</a></b>"
    return string


@dp.message_handler(text="ℹ️ Info")
async def info_about_bot(message: types.Message):
    await message.answer("Arizlarni qabul qiluvchi telegram bot\nYangliklarni @shermuhammadovfardu kanalida kuzatib boring")


@dp.message_handler(text="📝 Ariza")
async def ticket_handler(message: types.Message):
    try:
        user = await db.get_user(telegram_id=message.from_user.id)
        ticket = await db.get_ticket(user_id=user['id'])
        if ticket['status'] == 3:
            await message.answer("Sizda yuborilgan ariza mavjud. Iltimos javobni kuting ungacha ariza yuborolmaysiz!")
            return
    except Exception as err:
        print(err, 'Ariza olishda xatolik')
    markup = await ticket_type_keyboards()
    await message.answer("Ariza turini tanlang", reply_markup=markup)
    await Ticket.tickey_type.set()


@dp.message_handler(state=Ticket.tickey_type)
async def unknown_ticket_type(message: types.Message, state: FSMContext):
    await message.edit_reply_markup()
    markup = await ticket_type_keyboards()
    await message.answer("Iltimos, ariza turini tanlang", reply_markup=markup)


@dp.callback_query_handler(ticket_type_cd.filter(), state=Ticket.tickey_type)
async def get_ticket_type(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await call.answer(cache_time=1)
    await call.message.edit_reply_markup()
    ticket_type_id = callback_data.get("id")
    await state.update_data(ticket_type=ticket_type_id)
    await state.update_data(user_id=call.from_user.id)
    await call.message.answer("Ariza matnini yuboring", reply_markup=types.ReplyKeyboardRemove())
    await Ticket.text.set()


@dp.message_handler(state=Ticket.text)
async def get_ticket_text(message: types.Message, state: FSMContext):
    await state.update_data(text=message.text)
    await message.answer("Agar arizangiz rasmdan iborat bo'lsa rasm yuboring, yoki /skip buyrug'ini yuboring")
    await Ticket.file.set()


@dp.message_handler(state=Ticket.file, content_types='photo')
async def get__file(message: types.Message, state: FSMContext):
    xabar = await message.answer("Iltimos kuting ...")
    photo = message.photo[-1]
    link = await photo_link(photo)
    await state.update_data(file=link)
    data = await send_data(message, state)
    await xabar.delete()
    await message.answer(data, parse_mode='html', reply_markup=confirmation_keyboards)
    await Ticket.confirm.set()


@dp.message_handler(commands="skip", state=Ticket.file)
async def get__file(message: types.Message, state: FSMContext):
    data = await send_data(message, state)
    await state.update_data(file="")
    await message.answer(text=data, parse_mode='html', reply_markup=confirmation_keyboards)
    await Ticket.confirm.set()


@dp.message_handler(state=Ticket.file)
async def unknown_ticket_file(message: types.Message, state: FSMContext):
    await message.reply(text="Noto'g'ri amal bajarildi! Iltimos rasm yuboring, yoki tashlab o'tish uchun /skip buyrug'ini yuboring")


@dp.callback_query_handler(confirm_cd.filter(), state=Ticket.confirm)
async def confirm(call: types.CallbackQuery, callback_data: dict,
                  state: FSMContext):
    await call.answer(cache_time=1)
    confirm = callback_data.get("confirm")
    await call.message.edit_reply_markup()

    async with state.proxy() as data:
        ticket_type = data.get("ticket_type")
        file = data.get("file")
        text = data.get("text")
        user_id = data.get("user_id")

    user = await db.get_user(telegram_id=user_id)
    all_id = await db.get_all_ticket()
    if confirm == "confirm":
        ticket_id = check(all_id)
        try:
            await db.add_ticket(
                id=ticket_id,
                file=file,
                text=text,
                ticket_type=int(ticket_type),
                created_at=datetime.now(),
                user_id=user['id'],
            )
            await call.message.answer("✅ Xabaringiz muvaffaqiyatli "
                                      "jo'natildi",
                                      reply_markup=menu)
        except Exception as err:
            print(err)
            print("Ticketni bazaga saqashda xatolik yuz berdi!")
            await call.message.answer("Ma'lumotlaringizda xatlik mavjud "
                                      "iltimos qaytadan urinib ko'ring!",
                                      reply_markup=menu)
        finally:
            await state.finish()
    else:
        await call.message.answer("Bekor qilindi, qayta ariza berish uchun "
                                  "Ariza tugmasini bosing", reply_markup=menu)
    await state.finish()

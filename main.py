from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.storage import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import config as cfg
import logging
from db import Data

db = Data("database.db")

logging.basicConfig(level=logging.INFO)
bot = Bot(cfg.TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

class info_reg(StatesGroup):
    name = State()
    tell = State()
    other = State()



@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if message.chat.type == "private":
        if(not db.check_user(message.from_user.id)):
            db.add_user(message.from_user.id, message.from_user.first_name, message.from_user.username)
        db.delete_cashe(message.from_user.id)
        markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        button1 = types.KeyboardButton(cfg.but1)
        button2 = types.KeyboardButton(cfg.but2)
        button3 = types.KeyboardButton(cfg.but3)
        button4 = types.KeyboardButton(cfg.but4)
        markup.add(button1, button2, button3, button4)
        await message.answer(cfg.begin, reply_markup=markup)


@dp.message_handler(commands=['delete_cashe'])
async def delete_cashe(message: types.Message):
    if message.chat.type == "private":
        if db.check_adm(message.from_user.id) is True:
            db.delete_all_cashe()
            await message.answer(cfg.right_deal)
        else:
            await message.answer(cfg.false_deal)

@dp.message_handler(commands=['delete_orders'])
async def delete_cashe(message: types.Message):
    if message.chat.type == "private":
        if db.check_adm(message.from_user.id) is True:
            db.delete_all_orders()
            await message.answer(cfg.right_deal)
        else:
            await message.answer(cfg.false_deal)

@dp.message_handler(state=info_reg.name)
async def inforeg(message: types.Message, state: FSMContext):
    if message.chat.type == "private":
        markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        button1 = types.KeyboardButton(cfg.but1)
        button2 = types.KeyboardButton(cfg.but2)
        button3 = types.KeyboardButton(cfg.but3)
        button4 = types.KeyboardButton(cfg.but4)
        markup.add(button1, button2, button3, button4)
        if message.text == cfg.but5:
            await message.answer(cfg.return1, reply_markup=markup)
            db.delete_cashe(message.from_user.id)
            await state.reset_state()
        elif message.text == cfg.but6:
            await message.answer(cfg.cancel, reply_markup=markup)
            db.delete_cashe(message.from_user.id)
            await state.reset_state()
        else:
            if type(message.text) == str:
                if 2 <= len(message.text) <= 50:
                    db.add_name_cashe(message.from_user.id, message.text)
                    await message.delete()
                    await message.answer(cfg.register2)
                    await state.finish()
                    await info_reg.tell.set()
                else:
                    await message.answer(cfg.option_name_failed)
                    await info_reg.name.set()
            else:
                await message.answer(cfg.cancel_name)
                await info_reg.name.set()


@dp.message_handler(state=info_reg.tell)
async def inforeg1(message: types.Message, state: FSMContext):
    if message.chat.type == "private":
        try:
            markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
            button1 = types.KeyboardButton(cfg.but1)
            button2 = types.KeyboardButton(cfg.but2)
            button3 = types.KeyboardButton(cfg.but3)
            button4 = types.KeyboardButton(cfg.but4)
            markup.add(button1, button2, button3, button4)
            if message.text == cfg.but5:
                await message.answer(cfg.return1, reply_markup=markup)
                db.delete_cashe(message.from_user.id)
                await state.reset_state()
            elif message.text == cfg.but6:
                await message.answer(cfg.cancel, reply_markup=markup)
                db.delete_cashe(message.from_user.id)
                await state.reset_state()
            else:
                if message.text[0] == "+" and type(int(message.text[1:])) == int or type(int(message.text)) == int:
                    if 5 <= len(message.text) <= 50:
                        # db.delete_cashe(message.from_user.id)
                        db.add_tel_cashe(message.from_user.id, message.text)
                        await message.delete()
                        await message.answer(cfg.register3)
                        # await bot.send_message(chat_id="@haishinharcumner", text=f"Նոր գործարք`\nՏարբերակ: {option}\nԱնուն: {name}\nՀեռախոսահամար: {tel}")
                        await state.finish()
                        await info_reg.other.set()
                    else:
                        await message.answer(cfg.option_tel_failed)
                        await info_reg.tell.set()
                else:
                    await message.answer(cfg.cancel_number)
                    await info_reg.tell.set()
        except Exception as e:
            await message.answer(cfg.failed)
            print(f"[FAILED] {e}")

@dp.message_handler(state=info_reg.other, content_types=[types.ContentType.PHOTO, types.ContentType.DOCUMENT, 'text'])
async def other(message: types.Message, state: FSMContext):
    if message.chat.type == "private":
        markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        button1 = types.KeyboardButton(cfg.but1)
        button2 = types.KeyboardButton(cfg.but2)
        button3 = types.KeyboardButton(cfg.but3)
        button4 = types.KeyboardButton(cfg.but4)
        markup.add(button1, button2, button3, button4)
        if message.text == cfg.but5:
            await message.answer(cfg.return1, reply_markup=markup)
            db.delete_cashe(message.from_user.id)
            await state.reset_state()
        elif message.text == cfg.but6:
            await message.answer(cfg.cancel, reply_markup=markup)
            db.delete_cashe(message.from_user.id)
            await state.reset_state()
        else:
            try:
                if message.content_type == types.ContentType.PHOTO or message.content_type == types.ContentType.DOCUMENT:
                    option = db.set_cashe(message.from_user.id)[1]
                    name = db.set_cashe(message.from_user.id)[0]
                    tel = db.set_cashe(message.from_user.id)[2]
                    db.add_message(message.from_user.id, option, name, tel)
                    await bot.send_message(chat_id=cfg.group, text=f"Նոր գործարք`\nՏարբերակ: {option}\nԱնուն և ազգանուն: {name}\nՀեռախոսահամար: {tel}\nԱյլ:")
                    await message.answer(cfg.right, reply_markup=markup)
                    db.delete_cashe(message.from_user.id)
                    await state.finish()
                    if message.content_type == types.ContentType.PHOTO:
                        photos = message.photo[0].file_id
                        await bot.send_photo(chat_id=cfg.group, photo=photos)
                        await message.delete()
                    elif message.content_type == types.ContentType.DOCUMENT:
                        document = message.document.file_id
                        await bot.send_document(chat_id=cfg.group, document=document)
                        await message.delete()
                elif message.text:
                    option = db.set_cashe(message.from_user.id)[1]
                    name = db.set_cashe(message.from_user.id)[0]
                    tel = db.set_cashe(message.from_user.id)[2]
                    db.add_message(message.from_user.id, option, name, tel)
                    await bot.send_message(chat_id=cfg.group, text=f"Նոր գործարք`\nՏարբերակ: {option}\nԱնուն և ազգանուն: {name}\nՀեռախոսահամար: {tel}\nԱյլ: [Լրացուցիչ տեղեկություններ չկան]")
                    db.delete_cashe(message.from_user.id)
                    db.delete_cashe(message.from_user.id)
                    await message.answer(cfg.bac, reply_markup=markup)
                    await message.delete()
                    await state.finish()
                else:
                    option = db.set_cashe(message.from_user.id)[1]
                    name = db.set_cashe(message.from_user.id)[0]
                    tel = db.set_cashe(message.from_user.id)[2]
                    db.add_message(message.from_user.id, option, name, tel)
                    await bot.send_message(chat_id=cfg.group, text=f"Նոր գործարք`\nՏարբերակ: {option}\nԱնուն և ազգանուն: {name}\nՀեռախոսահամար: {tel}\nԱյլ: [Լրացուցիչ տեղեկություններ չկան]")
                    db.delete_cashe(message.from_user.id)
                    await message.answer(cfg.bac, reply_markup=markup)
                    await state.finish()
            except Exception as e:
                db.delete_cashe(message.from_user.id)
                print(f"[ERROR] {e}")
                await state.finish()
                await message.answer(cfg.error, reply_markup=markup)

@dp.message_handler()
async def default(message: types.Message):
    if message.chat.type == "private":
        if message.text == cfg.but1 or message.text == cfg.but2 or message.text == cfg.but3 or message.text == cfg.but4:
            try:
                markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
                button1 = types.KeyboardButton(cfg.but5)
                button2 = types.KeyboardButton(cfg.but6)
                markup.add(button1, button2)
                await message.answer(cfg.send_your_contact, reply_markup=markup)
                option = message.text
                db.delete_cashe(message.from_user.id)
                db.add_option(message.from_user.id, option)
                await message.answer(cfg.register1)
                await info_reg.name.set()
            except Exception as e:
                db.delete_cashe(message.from_user.id)
                print(e)
        elif message.text == cfg.but5:
            markup1 = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
            button1 = types.KeyboardButton(cfg.but1)
            button2 = types.KeyboardButton(cfg.but2)
            button3 = types.KeyboardButton(cfg.but3)
            button4 = types.KeyboardButton(cfg.but4)
            markup1.add(button1, button2, button3, button4)
            db.delete_cashe(message.from_user.id)
            await message.answer(cfg.return2, reply_markup=markup1)
        elif message.text == cfg.but6:
            db.delete_cashe(message.from_user.id)
            await message.answer(cfg.false_cancel)
        for hrm in cfg.hramanner:
            if message.text.upper() == hrm.upper():
                markup1 = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
                button1 = types.KeyboardButton(cfg.but1)
                button2 = types.KeyboardButton(cfg.but2)
                button3 = types.KeyboardButton(cfg.but3)
                button4 = types.KeyboardButton(cfg.but4)
                markup1.add(button1, button2, button3, button4)
                db.delete_cashe(message.from_user.id)
                await message.answer(cfg.begin, reply_markup=markup1)



if __name__ == "__main__":
    executor.start_polling(dp)


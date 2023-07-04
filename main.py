from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.storage import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import config as cfg
import logging
import time
from db import Data

db = Data("database.db")

logging.basicConfig(level=logging.INFO)

bot = Bot(cfg.TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

class info_reg(StatesGroup):
    name = State()
    tell = State()

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if message.chat.type == "private":
        if(not db.check_user(message.from_user.id)):
            db.add_user(message.from_user.id, message.from_user.first_name, message.from_user.username)

        markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        button1 = types.KeyboardButton(cfg.but1)
        button2 = types.KeyboardButton(cfg.but2)
        button3 = types.KeyboardButton(cfg.but3)
        button4 = types.KeyboardButton(cfg.but4)
        markup.add(button1, button2, button3, button4)
        await message.answer(cfg.begin, reply_markup=markup)


@dp.message_handler(state=info_reg.name)
async def inforeg(message: types.Message, state: FSMContext):
    if message.chat.type == "private":
        markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        button1 = types.KeyboardButton(cfg.but1)
        button2 = types.KeyboardButton(cfg.but2)
        button3 = types.KeyboardButton(cfg.but3)
        button4 = types.KeyboardButton(cfg.but4)
        markup.add(button1, button2, button3, button4)
        if message.text == "but6":
            await state.reset_state()
            await message.answer(cfg.cancel, reply_markup=markup)
        elif message.text == "but5":
            await state.reset_state()
            await message.answer(cfg.return1, reply_markup=markup)
        else:
            if type(message.text) == str:
                if 2 <= len(message.text) <= 50:
                    db.add_name_cashe(message.from_user.id, message.text)
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
            if message.text == "but6":
                await state.reset_state()
                await message.answer(cfg.cancel, reply_markup=markup)
            elif message.text == "but5":
                await state.reset_state()
                await message.answer(cfg.return1, reply_markup=markup)
            else:
                if message.text[0] == "+" and type(int(message.text[1:])) == int or type(int(message.text)) == int:
                    if 5 <= len(message.text) <= 50:
                        option = db.set_cashe(message.from_user.id)[1]
                        name = db.set_cashe(message.from_user.id)[0]
                        tel = message.text
                        db.add_message(message.from_user.id, option, name, tel)
                        db.delete_cashe(message.from_user.id)
                        await message.answer(cfg.right, reply_markup=markup)
                        await bot.send_message(chat_id="@haishinharcumner", text=f"Նոր գործարք`\nՏարբերակ: {option}\nԱնուն: {name}\nՀեռախոսահամար: {tel}")
                        await state.finish()
                    else:
                        await message.answer(cfg.option_tel_failed)
                        await info_reg.tell.set()
                else:
                    await message.answer(cfg.cancel_number)
                    await info_reg.tell.set()
        except Exception as e:
            await message.answer(cfg.failed)
            print(f"[FAILED] {e}")

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
                db.add_option(message.from_user.id, option)
                time.sleep(1)
                await message.answer(cfg.register1)
                await info_reg.name.set()
            except Exception as e:
                db.delete_cashe(message.from_user.id)
                print(e)


if __name__ == "__main__":
    executor.start_polling(dp)


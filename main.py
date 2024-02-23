import asyncio
import logging

from decouple import config


from aiogram import Bot, Dispatcher, Router, types,F
from aiogram.utils import keyboard
from aiogram.filters import CommandStart, Command   


TOKEN = config("TOKEN")

dp = Dispatcher() # объект диспетчера (оброботчик событий)
bot = Bot(TOKEN)

# async - асинхронная функция (позволяет не блокировать выполнение кода)
# await - ожидание выполнения асинхронной функции




kb_builder = keyboard.ReplyKeyboardBuilder()
kb_builder.button(text = "❤️Кнопка 1")
kb_builder.button(text = "🧡Кнопка 2")

kb_builder.button(text = "💚Кнопка 3")
kb_builder.adjust(2)
kb_builder.row(
    types.KeyboardButton(text = "💙Кнопка 4"),
    types.KeyboardButton(text = "💜Кнопка 5"),
)

menu_kb = types.ReplyKeyboardMarkup(keyboard=
[
    [
        types.KeyboardButton(text = "ВІДПРАВИТИ КОНТАКТ", request_contact=True),
    ],
    [
        types.KeyboardButton(text = "ВІДПРАВИТИ ГЕОЛОКАЦІЮ", request_location=True),
    ],
    [
        types.KeyboardButton(text = "❤️Кнопка 1"),
        types.KeyboardButton(text = "🧡Кнопка 2"),
    ],
    [
        types.KeyboardButton(text = "💚Кнопка 3"),
        types.KeyboardButton(text = "💙Кнопка 4"),
    ]
], resize_keyboard=True)

inline_kb = types.InlineKeyboardMarkup(inline_keyboard=[
    [
        types.InlineKeyboardButton(text="Кнопка 1", callback_data="button_1")
    ],
    [
        types.InlineKeyboardButton(text="Кнопка 2", callback_data="button_2")
    ],
    [
        types.InlineKeyboardButton(text="LMS", url="https://lms.ithillel.ua/"),
        types.InlineKeyboardButton(text="blog", url="https://blog.ithillel.ua/")
    ]
])

click_me_kb = keyboard.InlineKeyboardBuilder()
click_me_kb.button(text="🪙", callback_data="click_me")

users = [
]

def check_user_or_create(user_id):
    for user in users:
        if user["id"] == user_id:
            return user
    user = {
        "id": user_id,
        "count": 0
    }
    users.append(user)
    return user





@dp.message(CommandStart())
async def command_start_handler(message: types.Message):
    user = check_user_or_create(message.from_user.id)
    await message.answer(f"Hello, {message.from_user.full_name}!", reply_markup=inline_kb)
    await message.answer("Выберите кнопку", reply_markup=kb_builder.as_markup())

@dp.message(Command("users"))
async def command_users_handler(message: types.Message):
    top5 = sorted(users, key=lambda x: x["count"], reverse=True)[:5]
    text =""
    for i, user in enumerate(top5):
        text += f"{i+1}. {user['id']} - {user['count']}\n"
    await message.answer(f"Пользователи: {len(users)}\n\nТоп 5:\n{text}")
    
@dp.message(Command("game"))
async def command_game_handler(message: types.Message):
    user = check_user_or_create(message.from_user.id)
    
    await message.answer("Кликни меня", reply_markup=click_me_kb.as_markup())
    
@dp.callback_query(F.data=="click_me")
async def click_me_handler(query: types.CallbackQuery):
    user = check_user_or_create(query.from_user.id)
    user["count"] += 1
    await query.message.edit_text(f'Клікни мене!😮\nКількість кліків: {user["count"]}', reply_markup=click_me_kb.as_markup())
    
    

@dp.message(Command("delete"))
async def command_delete_handler(message: types.Message):
    await message.answer("Удаление клавиатуры", reply_markup=types.ReplyKeyboardRemove())

@dp.message(Command("menu"))
async def command_menu_handler(message: types.Message):
    await message.answer("Выберите кнопку", reply_markup=menu_kb)

@dp.message(F.text=="❤️Кнопка 1")
async def button_1_handler(message: types.Message):
    await message.answer("Вы нажали на кнопку 1")
    
@dp.message(F.text.in_(["🧡Кнопка 2", "💚Кнопка 3"]))
async def button_2_handler(message: types.Message):
    await message.answer("Вы нажали на кнопку 2 або 3")

##-----------------Inline Keyboard-----------------##
@dp.callback_query(F.data=="button_1")
async def inline_button_1_handler(query: types.CallbackQuery):
    await query.message.answer("Вы нажали на кнопку 1")

@dp.callback_query(F.data=="button_2")
async def inline_button_2_handler(query: types.CallbackQuery):
    await query.message.answer("Вы нажали на кнопку 2")
    
    
    
    

@dp.message(F.contact)
async def contact_handler(message: types.Message):
    await message.answer(f"Ваш контакт: {message.contact}")
    print(message.contact)

@dp.message(F.location)
async def location_handler(message: types.Message):
    await message.answer(f"Ваша геолокация: {message.location}")
    print(message.location)

@dp.message(Command("special_buttons"))
async def cmd_special_buttons(message: types.Message):
    builder = keyboard.ReplyKeyboardBuilder()
    # метод row позволяет явным образом сформировать ряд
    # из одной или нескольких кнопок. Например, первый ряд
    # будет состоять из двух кнопок...
    builder.row(
        types.KeyboardButton(text="Запросить геолокацию", request_location=True),
        types.KeyboardButton(text="Запросить контакт", request_contact=True)
    )
    # ... второй из одной ...
    builder.row(types.KeyboardButton(
        text="Создать викторину",
        request_poll=types.KeyboardButtonPollType(type="quiz"))
    )
    # ... а третий снова из двух
    builder.row(
        types.KeyboardButton(
            text="Выбрать премиум пользователя",
            request_user=types.KeyboardButtonRequestUser(
                request_id=1,
                user_is_premium=True
            )
        ),
        types.KeyboardButton(
            text="Выбрать супергруппу с форумами",
            request_chat=types.KeyboardButtonRequestChat(
                request_id=2,
                chat_is_channel=False,
                chat_is_forum=True
            )
        )
    )
    # WebApp-ов пока нет, сорри :(

    await message.answer(
        "Выберите действие:",
        reply_markup=builder.as_markup(resize_keyboard=True),
    )

@dp.message(F.poll)
async def poll_handler(message: types.Message):
    await message.answer(f"Вы создали викторину: {message.poll}")





async def main() -> None:
    await bot.set_my_commands([
        types.BotCommand(command="asd", description="Запуasdasdasdск бота"),
        types.BotCommand(command="start", description="Запуск бота"),
        types.BotCommand(command="help", description="Помощь"),
        types.BotCommand(command="menu", description="Меню"),
        types.BotCommand(command="delete", description="Удаление клавиатуры"),
        types.BotCommand(command="special_buttons", description="Специальные кнопки"),
    ], scope=types.BotCommandScopeAllPrivateChats())
    # await bot.set_my_commands([], scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot)


if __name__ == "__main__":
    # logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
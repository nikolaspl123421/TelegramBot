import asyncio
import logging
import random
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

# Включаємо логування
logging.basicConfig(level=logging.INFO)

TOKEN = "7316306574:AAFl2Gsp8nDcQ5NKRRk8GWiEcRUdkI8Ua5A"  # Замінити на реальний токен

bot = Bot(token=TOKEN)
dp = Dispatcher()
dp["bot"] = bot  # Передача бота в Dispatcher

# 🔹 Головне меню
# 🔹 Головне меню без кнопки "🔙 Назад"
menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🍽 Обрати кухню"), KeyboardButton(text="💳 Оплата")],
        [KeyboardButton(text="🔍 Переглянути стан рахунку")]
    ],
    resize_keyboard=True
)


# 🔹 База даних кухонь
complex_menus = {
    "asian": {
        "name": "🥢 Тайська кухня",
        "restaurant": "Golden Dragon",
        "street": "вул. Корзо, 17",
        "menu": "Том Ям з креветкою + Пад тай з кальмарами + Каном біанг (десерт) + Тропічний лимонад",
        "allergens": "Молочні продукти, томатна паста, морепродукти"
    },
    "mexican": {
        "name": "🌮 Мексиканська кухня",
        "restaurant": "El Sombrero",
        "street": "вул. Волошина, 12",
        "menu": "Чилі кон карне + Тако з куркою + Чурос реллено (десерт) + Аква фреска (фруктовий напій)",
        "allergens": "М’ясо, глютен, яйця"
    },
    "ukrainian": {
        "name": "🇺🇦 Українська кухня",
        "restaurant": "Смакота",
        "street": "пл. Корятовича, 5",
        "menu": "Борщ + Деруни з грибним соусом + Сирна запіканка + Узвар",
        "allergens": "Томати, м’ясо, гриби, молочні продукти, цитруси"
    },
    "italian": {
        "name": "🍝 Італійська кухня",
        "restaurant": "Pasta Bella",
        "street": "вул. Довженка, 22",
        "menu": "Мінестроне + Канелоні з фаршем + Панна котта з фруктовим соусом + Цитрусовий лимонад",
        "allergens": "Томати, глютен, молочні продукти, м’ясо, цитруси"
    },
    "american": {
        "name": "🍔 Фастфуд",
        "restaurant": "Burger Town",
        "street": "вул. Швабська, 33",
        "menu": "Чизбургер + Картопля фрі + Морозиво з фруктовим топінгом + Газований напій",
        "allergens": "Томати, гірчиця, глютен, молочні продукти, м’ясо"
    },
    "french": {
        "name": "🥖 Французька кухня",
        "restaurant": "Le Petit Bistro",
        "street": "вул. Грушевського, 8",
        "menu": "Вішісуаз (цибулевий суп) + Бургиньйон з яловичини + Плаваючий острів (десерт) + Ягідний лимонад",
        "allergens": "Молочні продукти, м’ясо, гриби, томати, глютен, яйця"
    },
    "indian": {
        "name": "🍛 Індійська кухня",
        "restaurant": "Curry House",
        "street": "вул. Капушанська, 14",
        "menu": "Дхал (суп із сочевиці) + Тікка масала + Гулаб джамун (десерт) + Лассі з манго",
        "allergens": "Молочні продукти, томати, м’ясо, цитруси, глютен"
    },
    "japanese": {
        "name": "🍣 Японська кухня",
        "restaurant": "Sakura Sushi",
        "street": "вул. Фединця, 19",
        "menu": "Місо + Ґьодзе зі свининою + Таякі (десерт) + Японська газована вода",
        "allergens": "Соєві боби, глютен, кунжут, м’ясо, яйця"
    },
    "greek": {
        "name": "🥗 Грецька кухня",
        "restaurant": "Aegean Breeze",
        "street": "вул. Легоцького, 27",
        "menu": "Сочевичний суп + Гірос + Галактобуреко (десерт) + Канелада",
        "allergens": "Глютен, м’ясо, томати, молочні продукти, цитруси"
    },
    "turkish": {
        "name": "🥙 Турецька кухня",
        "restaurant": "Istanbul Grill",
        "street": "вул. Гагаріна, 5",
        "menu": "Яйла чорбаси (йогуртовий суп) + Долма + Пахлава (десерт) + Гранатовий чай",
        "allergens": "Молочні продукти, яйця, глютен, м’ясо, горіхи, цитруси"
    }
}

# 🔹 База страв
dishes = {
    "asian": [{"name": "Рамен", "allergens": "Глютен, соя"}, {"name": "Суші-сет", "allergens": "Риба"}],
    "mexican": [{"name": "Тако", "allergens": "Глютен, молочні продукти"}],
    "ukrainian": [{"name": "Борщ", "allergens": "Селера"}],
    "italian": [{"name": "Піца Маргарита", "allergens": "Глютен, молочні продукти"}],
    "fastfood": [{"name": "Чізбургер", "allergens": "Глютен, сир"}],
    "french": [{"name": "Круасан", "allergens": "Глютен, масло"}],
    "indian": [{"name": "Карі з куркою", "allergens": "Гострі спеції"}],
    "japanese": [{"name": "Суші-сет", "allergens": "Риба, глютен"}],
    "greek": [{"name": "Грецький салат", "allergens": "Сир, оливкова олія"}],
    "turkish": [{"name": "Кебаб", "allergens": "М’ясо"}]
}

# 🔹 Обробка команди /start
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Привіт! Цей бот допоможе тобі смачно пообідати😉! Обери тип кухні або інші функції:", reply_markup=menu_keyboard)

# 🔹 Обробка кнопки "🍽 Обрати кухню"
@dp.message(lambda message: message.text == "🍽 Обрати кухню")
async def choose_cuisine(message: types.Message):
    buttons = [[InlineKeyboardButton(text=value["name"], callback_data=f"cuisine_{key}")] for key, value in complex_menus.items()]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer("Оберіть тип кухні:", reply_markup=keyboard)


# 🔹 Обробка вибору кухні
@dp.callback_query(lambda c: c.data.startswith("cuisine_"))
async def select_cuisine(callback_query: types.CallbackQuery):
    cuisine_key = callback_query.data.split("_")[1]

    if cuisine_key not in complex_menus:
        await callback_query.answer("⚠️ Ця кухня недоступна!", show_alert=True)
        return

    selected_menu = complex_menus[cuisine_key]
    price = random.randint(149, 499)  # 🔥 Випадкова ціна від 149 до 499 грн

    response = (
        f"🍽 {selected_menu['name']}\n"
        f"🏢 Ресторан: {selected_menu['restaurant']}\n"
        f"📍 Адреса: {selected_menu['street']}\n"
        f"📜 Меню: {selected_menu['menu']}\n"
        f"⚠️ Алергени: {selected_menu['allergens']}\n"
        f"💰 Ціна: {price} грн"
    )

    await callback_query.answer()
    await callback_query.message.answer(response)




# 🔹 Обробка кнопки "💳 Оплата"
@dp.message(lambda message: message.text == "💳 Оплата")
async def payment_info(message: types.Message):
    await message.answer("💰 Для оплати використовуйте картку або готівку в ресторані.\n\n"
                         "📍 Оплата доступна за адресою ресторану, де ви обрали страву.")

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

# 🔹 Клас для збереження стану користувача (введення балансу)
class AccountState(StatesGroup):
    entering_balance = State()

# 🔹 Обробка кнопки "🔍 Переглянути стан рахунку"
@dp.message(lambda message: message.text == "🔍 Переглянути стан рахунку")
async def check_balance(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    balance = user_data.get("balance")  # Отримуємо збережений баланс

    if balance is not None:
        # Якщо баланс є, виводимо його та пропонуємо змінити
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="🔄 Змінити баланс", callback_data="change_balance")]]
        )
        await message.answer(f"💳 Ваш поточний баланс: {balance} грн", reply_markup=keyboard)
    else:
        # Якщо балансу немає, просимо ввести його
        await state.set_state(AccountState.entering_balance)
        await message.answer("💰 Введіть суму грошей, які у вас є на обід:")

# 🔹 Обробка зміни балансу
@dp.callback_query(lambda c: c.data == "change_balance")
async def change_balance(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(AccountState.entering_balance)  # Запускаємо стан введення
    await callback_query.message.answer("💰 Введіть новий баланс:")
    await callback_query.answer()

# 🔹 Обробка введення суми користувачем
@dp.message(AccountState.entering_balance)
async def save_balance(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("⚠️ Введіть число без букв і символів!")
        return

    balance = int(message.text)
    await state.update_data(balance=balance)  # Зберігаємо баланс у пам’яті користувача
    await state.set_state(None)  # ВАЖЛИВО: Виходимо зі стану введення, щоб не зациклювалося

    await message.answer(f"✅ Ваш баланс встановлено: {balance} грн")

# 🔹 Обробка кнопки "🔙 Назад"
@dp.message(lambda message: message.text == "🔙 Назад")
async def go_back(message: types.Message):
    await message.answer("Ви повернулися в головне меню.", reply_markup=menu_keyboard)

# 🔹 Запуск бота
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

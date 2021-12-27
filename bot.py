from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from pars import pars
from canvas import make_a_pic_2
import requests

from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

answer = []

# flags
last_req = None
wait_title = False
wait_pos = False
wait_for_choose_photo = False
wait_for_req = False

# user choise
num_of_photos = 5
choosen_photo = None
choosen_pose = None
choosen_title = None

button1 = types.KeyboardButton("Сверху")
button2 = types.KeyboardButton("Посередине")

markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(button1, button2)

markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(types.KeyboardButton("/create"))

inline_btn2 = types.InlineKeyboardButton("Пожертвовать", callback_data="share")
inline_btn3 = types.InlineKeyboardButton("Заново", callback_data="again")

inline_kb1 = types.InlineKeyboardMarkup().add(inline_btn2, inline_btn3)


# query handlers
@dp.callback_query_handler(lambda c: c.data == 'again')
async def process_callback_again(callback_query: types.CallbackQuery):
    g = globals()
    g['wait_title'] = False
    g['wait_pos'] = False
    g['wait_for_choose_photo'] = False
    g['wait_for_req'] = True
    g['last_req'] = None
    await bot.send_message(callback_query.from_user.id, 'Что вам найти?')
    await bot.answer_callback_query(callback_query.id)


@dp.callback_query_handler(lambda c: c.data == "share")
async def process_callback_share(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, 'Еще не сделал')
    await bot.answer_callback_query(callback_query.id)



# hello
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply('Приветствую',reply_markup=markup1,reply=False)
    await bot.send_photo(message.from_user.id,
                         'https://api.deepai.org/job-view-file/0073cd5b-4a53-4d50-8239-7ce910681434/outputs/output.png',
                         "Пример ---  Введите /create чтобы начать")


# start process
@dp.message_handler(commands=['create'])
async def create(message: types.Message):
    await bot.send_message(message.from_user.id, 'Что вам найти?')
    g = globals()
    g['wait_title'] = False
    g['wait_pos'] = False
    g['wait_for_choose_photo'] = False
    g['wait_for_req'] = True
    g['last_req'] = None


# cancel
@dp.message_handler(commands=['cancel'])
async def create(message: types.Message):
    await bot.send_message(message.from_user.id, 'Что вам найти?')
    g = globals()
    g['wait_title'] = False
    g['wait_pos'] = False
    g['wait_for_choose_photo'] = False
    g['wait_for_req'] = True
    g['last_req'] = None


# cancel
@dp.message_handler(commands=['more'])
async def create(message: types.Message):
    g = globals()
    if g['last_req'] == None or g['wait_for_choose_photo'] == False:
        await bot.send_message(message.from_user.id, "Введите /create чтобы начать")
    else:
        g['num_of_photos'] += 5
        await bot.send_message(message.from_user.id, 'Момент...')
        answer = pars(g['last_req'], g['num_of_photos'])
        g['answer'] = answer
        i = 1
        for el in answer:
            await bot.send_photo(message.from_user.id, el, i)
            i += 1
        await bot.send_message(message.from_user.id, 'Что выберете? или еще(/more)?\n /cancel чтобы сбросить')


# handler
@dp.message_handler()
async def take(message: types.Message):
    g = globals()
    # wait for request
    if wait_for_req:
        g['wait_for_req'] = False
        g['wait_for_choose_photo'] = True
        await bot.send_message(message.from_user.id, 'Момент...')
        answer = pars(message.text)
        g['answer'] = answer
        g['last_req'] = message.text
        i = 1
        for el in answer:
            await bot.send_photo(message.from_user.id, el, i)
            i += 1
        await bot.send_message(message.from_user.id, 'Что выберете из ' + str(
            g['num_of_photos']) + '? или еще(/more)?\n /cancel чтобы сбросить')
    # wait for choose
    elif wait_for_choose_photo:
        g['wait_for_choose_photo'] = False
        g['wait_title'] = True
        try:
            if g['num_of_photos'] >= int(message.text) > 0:
                await bot.send_message(message.from_user.id, 'Что напишем?\n /cancel чтобы сбросить')
                answer = g['answer']
                g['choosen_photo'] = answer[int(message.text) - 1]
                p = requests.get(g['choosen_photo'])
                out = open('./img/img.jpg', "wb")
                out.write(p.content)
                out.close()
            else:
                await bot.send_message(message.from_user.id, 'Укажите номер изображения\n /cancel чтобы сбросить')
                g['wait_for_choose_photo'] = True
                g['wait_title'] = False
        except:
            await bot.send_message(message.from_user.id, 'Укажите номер изображения\n /cancel чтобы сбросить')
            g['wait_for_choose_photo'] = True
            g['wait_title'] = False
    # wait for choose
    elif wait_title:
        g['wait_title'] = False
        g['wait_pos'] = True
        # print(message.text)
        g['choosen_title'] = message.text

        await bot.send_photo(message.from_user.id,
                             'https://api.deepai.org/job-view-file/6a1298f5-c071-4422-a916-11ebe0ca1165/outputs/output.png')
        await bot.send_photo(message.from_user.id,
                             'https://api.deepai.org/job-view-file/960dd8f1-98c5-4ebe-b04e-e9b30c7e0d36/outputs/output.png')
        await message.reply("Где напишем?", reply_markup=markup,reply=False)
    elif wait_pos:
        g['wait_pos'] = False
        # try:
        if message.text == 'Сверху':
            num = 1
        elif message.text == 'Посередине':
            num = 2
        else:
            g['wait_pos'] = True
            await message.reply("Где напишем?", reply_markup=markup,reply=False)
        g['choosen_pos'] = num
        # shalay balalay
        await bot.send_message(message.from_user.id, 'Происходит магия...')
        pic_url = make_a_pic_2(num=int(g['choosen_pos']) - 1, text=g['choosen_title'])
        await bot.send_photo(chat_id=message.from_user.id, photo=pic_url)
        await message.reply("Что дальше?", reply_markup=inline_kb1,reply=False)

        # await bot.send_photo(message.from_user.id, './img/new_img.jpg',
        #                      'Cкачать\n /create чтобы начать заново')
        g['wait_title'] = False
        g['wait_pos'] = False
        g['wait_for_choose_photo'] = False
        g['wait_for_req'] = True
        g['last_req'] = None
    else:
        await message.reply("Введите /create чтобы начать",reply=False)


    if __name__ == '__main__':
        executor.start_polling(dp)

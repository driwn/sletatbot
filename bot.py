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


# hello
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply('Приветствую')
    await bot.send_photo(message.from_user.id, 'https://api.deepai.org/job-view-file/ad8c42f0-8bb5-4504-af3f-aa43f257a21e/outputs/output.png', "Пример ---  Введите /create чтобы начать")


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
            if int(message.text) <= g['num_of_photos'] and int(message.text) > 0:
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
        if len(message.text) > 15:
            g['wait_title'] = True
            g['wait_pos'] = False
            await bot.send_message(message.from_user.id, 'Cлишком длинная фраза\n /cancel чтобы сбросить')
        else:
            g['choosen_title'] = message.text

            await bot.send_photo(message.from_user.id, 'https://api.deepai.org/job-view-file/63b76665-ba1d-4424-9efe-f22e38fa5a58/outputs/output.png',1)
            await bot.send_photo(message.from_user.id,'https://api.deepai.org/job-view-file/8bc81d18-8c04-4396-8361-4e0549f318cc/outputs/output.png',2)
            await bot.send_photo(message.from_user.id, 'https://api.deepai.org/job-view-file/0fa9d190-1a7f-4b02-9666-c956be817d89/outputs/output.png', 3)
            await bot.send_message(message.from_user.id, 'Где напишем?(1-3)\n /cancel чтобы сбросить')
    elif wait_pos:
        g['wait_pos'] = False
        # try:
        if message.text == '1' or message.text == '2' or message.text == '3' or message.text == '4':
            g['choosen_pos'] = message.text
            # shalay balalay
            await bot.send_message(message.from_user.id, 'Происходит магия...')
            pic_url = make_a_pic_2(num=int(g['choosen_pos'])-1,text=g['choosen_title'])
            await bot.send_photo(chat_id=message.from_user.id,photo=pic_url)
            # await bot.send_photo(message.from_user.id, './img/new_img.jpg',
            #                      'Cкачать\n /create чтобы начать заново')
            g['wait_title'] = False
            g['wait_pos'] = False
            g['wait_for_choose_photo'] = False
            g['wait_for_req'] = True
            g['last_req'] = None
        else:
            g['wait_pos'] = True
            await bot.send_message(message.from_user.id, 'Укажите номер варианта\n /cancel чтобы сбросить')
        # except:
        #     g['wait_pos'] = True
        #     await bot.send_message(message.from_user.id, 'Укажите номер варианта\n /cancel чтобы сбросить')
    else:
        await message.reply("Введите /create чтобы начать")


if __name__ == '__main__':
    executor.start_polling(dp)

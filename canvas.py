from PIL import Image, ImageDraw, ImageFont

from time import sleep
import requests

txt_bg = Image.open('img/backgrnd.png')
logo = Image.open('img/s.png')
ch_bg = Image.open('img/cletat fon for leters.png')

variants = [
    {
        "name": "top",
        "bg_w": 0.9,
        "bg_h": 0.2,
        "bg_x": 0.08,
        "bg_y": 0.1
    },
    {
        "name": "bottom",
        "bg_w": 0.9,
        "bg_h": 0.2,
        "bg_x": 0.08,
        "bg_y": 0.80
    },
    {
        "name": "center",
        "bg_w": 0.9,
        "bg_h": 0.2,
        "bg_x": 0.08,
        "bg_y": 0.4
    },
]


def make_a_pic_2(num=2, url='./img/img.jpg', text="123445677886"):
    text = text.upper()
    v = variants[num]
    sleep(0.5)

    img = Image.open(url)
    height = img.size[1]
    width = img.size[0]
    # print(height, width)
    if width < height:
        height = width
    # print(height, width)
    font = ImageFont.truetype('Maler.ttf', round(height * 0.08))

    new_img = Image.new("RGB", (height, height))

    draw = ImageDraw.Draw(new_img)

    new_img.paste(img)
    new_txt_bg = txt_bg.resize((round(height * v["bg_w"]), round(height * v["bg_h"])))
    new_logo = logo.resize((round(height * 0.15), round(height * 0.15)))
    new_img.paste(new_logo, (-5, 5), new_logo)

    new_img.paste(new_txt_bg, (round(height * v['bg_x']), round(height * v['bg_y'])), new_txt_bg)
    draw.multiline_text((height // 3.2, round(height * (v['bg_y'] + 0.05))), text, font=font, align='center',
                        fill="#db9200")

    new_img.save("./img/new_img.jpg")

    r = requests.post(
        "https://api.deepai.org/api/waifu2x",
        files={
            'image': open('./img/new_img.jpg', 'rb'),
        },
        headers={'api-key': 'fddf0e74-3601-4ccd-abde-3f55786675f9'}
    )
    print(r.json())
    return r.json()['output_url']

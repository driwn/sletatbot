from PIL import Image, ImageDraw, ImageFont
from time import sleep
import requests

logo = Image.open('img/s.png')
ch_bg = Image.open('img/f.png')

variants = [
    {
        "name": "top",
        "bg_w": 0.9,
        "bg_h": 0.2,
        "bg_x": 0.09,
        "bg_y": 0.08
    },
    {
        "name": "center",
        "bg_w": 0.9,
        "bg_h": 0.2,
        "bg_x": 0.09,
        "bg_y": 0.4
    },
    {
        "name": "bottom",
        "bg_w": 0.9,
        "bg_h": 0.2,
        "bg_x": 0.09,
        "bg_y": 0.80
    }

]


def make_a_pic_2(num=2, url='./img/img.jpg', text="123445677886"):

    while "\n" in text:
        text = text.replace("\n"," ---")
    text = text.upper()
    text = text+" "

    v = variants[num]
    sleep(0.5)

    img = Image.open(url)
    height = img.size[1]
    width = img.size[0]
    if width < height:
        height = width
    font = ImageFont.truetype('Maler.ttf', round(height*0.08))

    new_img = Image.new("RGB", (height, height))

    draw = ImageDraw.Draw(new_img)

    new_img.paste(img)
    ch_bg_r = ch_bg.resize((round(height*0.15),round(height*0.15)))
    new_logo = logo.resize((round(height * 0.15), round(height * 0.15)))
    new_img.paste(new_logo, (-5, 5), new_logo)

    more_h = 0
    i=0
    while i < len(text):
        x=0
        while x <= 13 and i < len(text)-1:
            if text[i]=="-":
                if text[i]+text[i+1]+text[i+2]=="---":
                    x=0
                    i+=3
                    more_h += round(height * 0.09)
                    continue
            if text[i]==" " and text.find(' ', i+2)-i > 14-x:
                x = 0
                i += 1
                more_h += round(height * 0.09)
                continue
            new_img.paste(ch_bg_r,
                          (round(height // 9 + x * round(height * 0.053)),
                              more_h + round(height * (v['bg_y'] + 0.03))),
                          ch_bg_r)
            x += 1
            i+=1
        more_h += round(height * 0.09)
        i+=1
    r=0
    more_h = 0
    while r < len(text):
        t=0
        while t <= 13 and r < len(text)-1:
            if text[r]=="-":
                if text[r]+text[r+1]+text[r+2]=="---":
                    t=0
                    r+=3
                    more_h += round(height * 0.09)
                    continue
            if text[r]==" " and text.find(' ', r+2)-r > 14-t:
                t = 0
                r += 1
                more_h += round(height * 0.09)
                continue
            draw.multiline_text((height//7+t*round(height*0.053),
                                     more_h+round(height*(v['bg_y']+0.05))),
                                    text[r], font=font, align='center', fill="#db9200")
            t += 1
            r+=1
        more_h += round(height * 0.09)
        r+=1

    # for i in range(len(text)):
    #
    #     new_img.paste(ch_bg_r, (round(height // 8+ i * round(height * 0.053)*f*s), more_h+round(height * (v['bg_y'] + 0.03))),ch_bg_r)
    #     if i>11:
    #         more_h=round(height*0.08)
    # more_h = 0
    # for i in range(len(text)):
    #     draw.multiline_text((height//6+i*round(height*0.053)*f*s,more_h+round(height*(v['bg_y']+0.05))), text[i], font=font, align='center', fill="#db9200")
    #     if i>11:
    #         more_h=round(height*0.08)


    new_img.save("./img/new_img.jpg")
    # new_img.show()
    r = requests.post(
        "https://api.deepai.org/api/waifu2x",
        files={
            'image': open('./img/new_img.jpg', 'rb'),
        },
        headers={'api-key': 'fddf0e74-3601-4ccd-abde-3f55786675f9'}
    )
    print(r.json())
    return r.json()['output_url']


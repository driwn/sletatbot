import requests
from time import sleep
from bs4 import BeautifulSoup as Bs


def pars(req='отель', ph=5):
    r = requests.get('https://yandex.ru/images/search?from=tabbar&text=' + str(req))
    sleep(1)
    html = Bs(r.content, 'html.parser')
    content = html.select('.serp-item')
    links = []
    for i in range(ph):
        s = content[i].get('data-bem')
        nurl = s.find('url')
        endoforl = s.find('"', nurl + 6)
        url = s[nurl + 6:endoforl]
        links.append(url)

    return links

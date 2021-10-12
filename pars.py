import requests
from time import sleep
from bs4 import BeautifulSoup as BS
def pars(req='отель',ph=5):
    r = requests.get('https://yandex.ru/images/search?from=tabbar&text=' + str(req))
    sleep(1)
    html = BS(r.content, 'html.parser')
    content = html.select('.serp-item')
    links=[]
    for i in range(ph):
        s = content[i].get('data-bem')
        nOURL = s.find('url')
        endOfUrl = s.find('"', nOURL + 6)
        url = s[nOURL + 6:endOfUrl]
        links.append(url)
        # p = requests.get(url)
        # # out = open('./img/'+str(i) + '.jpg', "wb")
        # # out.write(p.content)
        # # out.close()

    return links

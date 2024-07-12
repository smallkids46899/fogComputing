import os
import requests
from bs4 import BeautifulSoup
from termcolor import colored
import pickle
import xlrd, xlwt
import math

real_domain='https://www.chipdip.ru/'
domain = 'https://www.chipdip.ru/catalog/elektrotekhnika'








def get_links():
    page = requests.get(domain)
    soup = BeautifulSoup(page.text, 'lxml')
    soup=soup.find_all('li', {'class':'catalog__item'})
    links=[]
    for s in soup:
        links.append(s.a.get('href'))
    get_tov_links(links )    # Убрать 1 !!!!!!!!!!


def get_tov_links(links):

    for link in links[363:]:
        for i in range(100):

            u=str(i)
            if u=='0':
                lin = real_domain + link
            else:

                try:
                    lin = real_domain + link + '?page=' + u
                    page = requests.get(lin)
                except:
                    print("a")
                    break
                soup = BeautifulSoup(page.text, 'lxml')
                soup = soup.find_all('div', {'class': 'item__name'})
                for s in soup:
                    hr = s.a.get('href')
                    with open('fffF.txt', 'a') as f:
                        f.write(hr + '\n')


# get_links()

mas=[]





def pars_tovars():
    with open('fff.txt', 'r') as f:
        mas = f.readlines()
        m = [i.strip('\n') for i in mas]
        linkS_and_par=[]
    print("Go")







    m=m[34560:]
    params_names=[]
    spisok_parametr=[] # список словарей параметров
    file_number = 24
    kol_m=math.ceil(len(m)/10)              #Мутим, чтобы ОЗУ не усмерло, делим все материалы в группы по кэсу
    print(kol_m)
    triger_new_page=True
    k=0
    for kol in range(kol_m):
        k=0

        if triger_new_page:
            wb = xlwt.Workbook()
            ws = wb.add_sheet('Test1', cell_overwrite_ok=True)
            ws.write(0, 0, "Категория 1")
            ws.write(0, 1, "Категория 2")
            ws.write(0, 2, "Категория 3")
            ws.write(0, 3, "Описание")
            ws.write(0, 4, "Цена")
            ws.write(0, 5, "Фото")
            ws.write(0, 6, "Ссылка")
            count_str = 1
            triger_new_page=False



        spisok_parametr = []
        linkS_and_par = []

        for i in m[kol*10:kol*10+9]:
            link_and_parms = []
            # print(kol * 100, kol * 100 + 100)

            try:
                link = real_domain + i

                page = requests.get(link)
                soup = BeautifulSoup(page.text, 'lxml')
                table = soup.find('table', {'class': 'product__params'})
                tr = table.find_all('tr')
                params = {}
                for t in tr:
                    try:
                        td = t.find_all('td')
                        params[td[0].text] = td[1].text
                    except:
                        break
                spisok_parametr.append(params)
                h1 = soup.find('h1')
                name = h1.text
                price = soup.find('span', {'class': 'ordering__value'})
                pr = price.text
                image = soup.find('div', {'class': 'item__image_medium_wrapper'})
                im = image.img
                im = im.get('src')
                categs = soup.find_all('a', {'class': 'no-visited bc__item_link link link_dark'})
                categ1 = categs[2].text
                categ2 = categs[3].text

                categ0 = 'Электротехника'
                link_and_parms.append(categ0)
                link_and_parms.append(categ1)
                link_and_parms.append(categ2)
                link_and_parms.append(name)
                link_and_parms.append(pr)
                link_and_parms.append(im)
                link_and_parms.append(link)
                linkS_and_par.append(link_and_parms)
                # print(link_and_parms)




            except:
                continue




        count = 0

        print(linkS_and_par)
        for link in linkS_and_par:
            count_str+=1
            for l in link:
                ws.write(count_str, count, l)
                count += 1

                if count == 7:
                    p = spisok_parametr[linkS_and_par.index(link)]
                    for par, val in p.items():
                        if par not in params_names:
                            params_names.append(par)

                        try:
                            index = params_names.index(par)
                            ws.write(count_str, index + 7, val)
                        except ValueError:
                            file_number+=1
                            triger_new_page = True
                            params_names=[]
                            k=1
                            break

                    count = 0




        count_par = 7

        if params_names!=[]:
            for p in params_names:
                try:
                    ws.write(0, count_par, p)
                except ValueError:
                    file_number += 1
                    triger_new_page = True
                    params_names = []
                    break

                count_par += 1


        template = "Vivod/Vivod{file_n}.xls"
        file_number_str=str(file_number)
        file = template.format(file_n=file_number_str)
        wb.save(file)

















pars_tovars()




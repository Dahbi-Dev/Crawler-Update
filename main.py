from tkinter import *
import tkinter.ttk
from lxml import html
import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import *
from time import sleep
import csv
import os
import re

with open(f'C:\\Users\\DELL\\Desktop\\update7.csv', 'w',newline='') as file:
    file.write("Catégorie; Nom de produit; Référence; Prix achat; Prix de vendre; Disponibilité; Description \n")




def getUpdateData(event):
    AccountCombo['values'] = dictionnaire[CategoryCombo.get()]
    AccountCombo.current(0)


def prog():
    user = "sensitive data"
    password = "sensitive data"
    category = str(CategoryCombo.get())
    sub = str(AccountCombo.get())
    Marge = number4.get()
    if 0 <= Marge and Marge < 100:
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.maximize_window()
        driver.implicitly_wait(5)
        driver.get('https://www.disway.com/profile/login')
        driver.find_element("id","Login_v3f4dtau5_email").send_keys(user)
        driver.find_element("id","Login_v3f4dtau5_password").send_keys(password)
        driver.find_element("xpath",'//*[@id="content"]/div[2]/div/div/div/div[1]/div/div[3]/form/div[4]/button').click()
        url = driver.find_element("xpath", f"//*[contains(text(),'{category}')]").get_attribute('href')
        driver.get(url)
        url = driver.find_element("xpath", f"//*[contains(text(),'{sub}')]").get_attribute('href')
        driver.get(url)
        """
        driver.get('https://www.disway.com/ordinateur/pc-portable/')
        """

        category = str(CategoryCombo.get())

        for k in range(20):
            sleep(2)

            category = str(CategoryCombo.get())
            titre = driver.find_elements("xpath",'//div[@class="PLP_product-description"]/a/h2/')
            reference = driver.find_elements("xpath",
                '//div[@class="PLP_product-id-stock"]/span[@class="PLP_product-id-name"]')
            prixachat = driver.find_elements("xpath",
                '//div[@class="Grid_col-auto Grid_align-self-auto price-block"]/span[@class="ProductPrice_actual-price actual-price"]')
            dispo = driver.find_elements("xpath",
                '//div[@class="PLP_product-id-stock"]/span[@class="PLP_stock-indication"]/span/text()')
            description = driver.find_elements("xpath",'//div[@class="PLP_product-attributes"]/text()')

            with open(f'C:\\Users\\DELL\\Desktop\\update7.csv', 'a', newline='') as file:
                sleep(2)
                for i in range(len(titre)):
                    Marge = number4.get()
                    prix = prixachat[i].text
                    prix = prix[0:-3]
                    prix = prix.replace('.', ' ')
                    prix = prix.replace(' ', '')
                    prix = prix.replace(',', '.')
                    prixf = float(prix)
                    prixf = round(prixf, 2)
                    prix_vente = prixf / ((100 - Marge) / 100)
                    prix_vente = round(prix_vente, 2)
                    prix_vente = str(prix_vente)
                    ref = reference[i].text
                    # ref = ref[9:]
                    
                    sleep(2)

                    file.write(category + "->" + sub + ";" + titre[i].text.replace("\n","") + ";" + ref + ";" + prix + ";" + prix_vente + ";" +dispo[i].text + ";" + description[i].text.replace("\n", " |") + "\n")

            sleep(2)
            next = driver.find_element("xpath",
                '//div[@class="Paging_pagination pagination"]/a[@class="Button_base Button_small Paging_arrow Paging_right"]')
            next.click()

        file.close()

        driver.quit()



    
    category = str(CategoryCombo.get())
index = "https://www.disway.com/"
p = requests.get(index)
pages_s = []
script = html.fromstring(p.content, parser=html.HTMLParser(encoding='utf8'))
pages_s.extend(script.xpath( '//*[@id="161qqzflz_7ea42b1d-f4c2-41af-9908-eaaec09f308c"]/li/a/text()'))
pages_s.extend(script.xpath('//*[@id="161qqzflz_7ea42b1d-f4c2-41af-9908-eaaec09f308c"]/li/ul/li/a/text()'))

# print(pages_s)
dictionnaire = {}
dictionnaire[pages_s[0]] = pages_s[5:9]
dictionnaire[pages_s[1]] = pages_s[9:17]
dictionnaire[pages_s[2]] = pages_s[17:22]
dictionnaire[pages_s[3]] = pages_s[22:29]
dictionnaire[pages_s[4]] = pages_s[29:43]

# print(dictionnaire[0])


root = Tk()
root.title('Disway')
root.configure(background='black')
root.geometry("350x290")
root.resizable(0,0)
Label(root, text='Adresse mail :', bg='black', fg='white').place(x=60, y=30)
number0 = StringVar()
number0.set('a.rodriguez@brioss.ma')
us = Entry(root, textvariable=number0)
us.place(x=155, y=30)
Label(root, text='Password :', bg='black', fg='white').place(x=60, y=60)
number1 = StringVar()
number1.set('Dbtrkp21Esp')
us = Entry(root, textvariable=number1)
us.place(x=155, y=60)

Label(root, text='Category :', bg='black', fg='white').place(x=60, y=90)
Label(root, text='Sub :', bg='black', fg='white').place(x=60, y=120)

AccountCombo = tkinter.ttk.Combobox(width=15)
AccountCombo.place(x=155, y=120)

CategoryCombo = tkinter.ttk.Combobox(width=15, values=list(dictionnaire.keys()))
CategoryCombo.bind('<<ComboboxSelected>>', getUpdateData)
CategoryCombo.place(x=155, y=90)

Label(root, text='La Marge :', bg='black', fg='white').place(x=60, y=150)
number4 = IntVar()
us = Entry(root, textvariable=number4)
us.place(x=155, y=160)
Button(root, text='star', width=10, bg='yellow', fg='black', command=prog).place(relx=0.5, rely=0.7, anchor=CENTER)
Button(root, text="Quit", width=10, bg='yellow', fg='black', command=root.destroy).place(relx=0.8, rely=0.7,
                                                                                         anchor=CENTER)
root.mainloop()



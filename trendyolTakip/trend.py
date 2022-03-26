from tokenize import Special
import requests
from bs4 import BeautifulSoup
from send_email import sendMail
import time
from_Mail=input("Kullanacağınız mail adresini giriniz: ")
mail_sifre=input("Kullanacağınız mail adresinin şifresini giriniz:")
url1=input("Takip etmek istediğiniz ürünün sayfa linkini giriniz: ")
baz_fiyat=float(input("Baz alacağınız fiyatı giriniz: "))
mytitle=input("Almak istediğiniz başlığın class'ını giriniz: ")
myprice=input("Almak istediğiniz fiyat değerinin class'ını giriniz: ")
myimage=input("Almak istediğiniz fotoğrafın class'ını giriniz: ")
sure=int(input("Kaç saatte bir kontrol edilmesi gerektiğini belirtiniz: "))
mymail=input("Hangi e-posta adresine bildirim gönderilmesini istiyorsunuz?:")
def checkPrice(url,paramPrice,my_title,my_price,my_image):
        
    headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"}
    
    
    page=requests.get(url, headers=headers)
    
    htmlPage=BeautifulSoup(page.content,'html.parser')
    
    productTitle=htmlPage.find("h1",class_=str(my_title)).getText()
    
    price=htmlPage.find("span",class_=str(my_price)).getText()
    
    image=htmlPage.find("img",class_=str(my_image))
    global convertedPrice
    convertedPrice = float(price.replace(",",".").replace("TL",""))
    if(convertedPrice<=paramPrice):
        print("Ürün fiyatı düştü")
        htmlEmailContent="""\
            <html>
            <head></head>
            <body>
            <br/>
            <h3>{0}</h3>
            <br/>
            {1}
            <br/>
            <p>Ürün linki: {2}</p>
            </body>
            </html>
            """.format(productTitle,image,url)
        sendMail(mymail,"Ürünün fiyatı düştü",htmlEmailContent)
        print(convertedPrice)
    else:
        print("Ürünün fiyatı düşmedi.")

while(True):
    checkPrice(url1,baz_fiyat,mytitle,myprice,myimage)
    if(convertedPrice<=baz_fiyat):
        break
    time.sleep(360*sure)
    
#Author:Mr.Programmer
#طبق گفته استاد در ویدیو پروژه در دو اسکریپت نوشته شد
#*******************************اسکریپت استخراج اطلاعات در دیتابیس مورد نظر*******************************
#لطفا قبل از ران کردن برنامه دیتابیسی با نام دلخواه بسازید که به شکل زیر متغیر بگیرد
#شرح کار برنامه:
#برنامه مناسب کاربرهاییست که میخواهند قیمت ماشین خود را ارزیابی کنند
#در این برنامه سعی می شود با استفاده از سایت تروکار اطلاعات قیمت کارکرد سال تولید ماشین های مطابق با برند و مدل درخواستی کاربر 
#در دیتابیسی که از قبل توسط کاربر با فرم زیر ساخته شده ذخیره کند
#CREATE TABLE نام تیبل (brand VARCHAR(100),model VARCHAR(100),year VARCHAR(100),mileage VARCHAR(100),price VARCHAR(100))
#سپس در اسکریپت دوم برنامه با دریافت برند و مدل خودروی شخصی کاربر قیمت ماشین را حدس میزند
#با تشکر از همکاری شما
from bs4 import BeautifulSoup
import requests
import mysql.connector
import re
fullname=[]
mileall=[]
yearall=[]
priceall=[]
#لطفا از طریق آدرس زیر به منوی سرچ سایت رجوع کنید و برند و مدل ها را چک کنید و مشابه آنها در اینپوت ها وارد کنید(بدون فاصله)
#https://www.truecar.com/used-cars-for-sale/
#لطفا برای اطمینان بیشتر سرچ را انجام داده تا مطمئن شوید که چگونه وارد کنید .
#در برند و مدل های چندتیکه ای ممکن است شما اشتباه کنید!
#وارد کردن نام برند ماشین
brnd=input('Please insert Your WantedCar BRAND in lowecase (for example:\'bmw\') : ')
#وارد کردن نام مدل ماشین
mdl=input('Please insert Your WantedCar MODEL in lowecase without space (for example:\'7-series\') : ')
#دریافت عدد از کاربر که چند صفحه ابتدایی را میخواهد؟
wantedpage=int(input('Please indicate how many front pages you want?(from \'1\' to \'your entered number\') : \n'))
#دسترسی به اطلاعات سیستمی و دیتابیسی کاربر
clientHOST=input('please enter your host : ')
clientUSER=input('please enter your user : ')
clientPASS=input('please enter your password : ')
clientDATABASE=input('please enter your database : ')
clientdatabaseTABLE=input('please enter your databaseTABLE : ')
print('please be Patience ...... \n . \n . \n . \n . \n . \n .')
#پیدا کردن تگ های مورد نظر در تعداد صفحه ابتدایی خواسته شده
for page in range(1,wantedpage):
    #ساخت ادرس سایت
    address='https://www.truecar.com/used-cars-for-sale/listings/'+brnd+'/'+mdl+'/?page='+str(page)
    #درخواست به سایت
    r=requests.get(address)
    #دسترسی به کد های سایت
    soup=BeautifulSoup(r.content,'html.parser')
    #ساختن شرط برای اطمینان از اینکه همچین صفحه ای وجود داشته باشد
    null_page=soup.find("span", {"class": "d-none d-md-block"})
    #اگر صفحه خالی باشد متغیر نال پیج شامل یکسری اطلاعات می شود 
    #پس شرط میزاریم که اگر صفحه مورد نظر خالی نبود(وجود داشت) اطلاعات خواسته شده را دریافت کن
    if not(null_page):
        #اضافه کردن اطلاعات به لیست ها
        #لیست فول نیم شامل برند و مدل است که بعدا تفکیک می شوند
        fullname.append(soup.findAll("span", {"class": "vehicle-header-make-model text-truncate"}))
        #لیست سال ساخت
        yearall.append(soup.findAll("span", {"class": "vehicle-card-year font-size-1"}))
        #لیست کارکرد ماشین
        mileall.append(soup.findAll("div", {"data-test": "vehicleMileage"}))
        #لیست قیمت که میتواند با قیمت یا بدون قیمت باشد 
        priceall.append(soup.findAll("div", {"class": "padding-left-3 padding-left-lg-2 vehicle-card-bottom-pricing-secondary vehicle-card-bottom-max-50"}))
    else:
        #اگر صفحه خالی بود(وجود نداشت) از حلقه بیرون بپر و چیزی ذخیره نکن
        #و وانتدپیج را برابر با شماره پیج قبلی (که وجود داشت) قرار بده
        #چون در مراحل بعدی از متغیر وانتد پیج استفاده میشود
        wantedpage=page-1
        print('The number of pages you requested did not exist. %i pages found and saved.'%wantedpage)
        break
#ساخت لیست ها نهایی
brand=[]
model=[]
year=[]
mile=[]
price=[]
#تفکیک کامل
for page in range(wantedpage-1):
    for num in range(len(fullname[page])):
        #گذاشت شرط برای اینکه ماشین بدون قیمت در داده ها ذخیره نکنیم
        if('$' in priceall[page][num].text):
            #تفکیک لیست فول نیم به دو بخش مدل و برند و اضافه کردنشان به لیست نهایی
            full=str(fullname[page][num].text).split(' ')
            brandname=full[0].lower()
            modelname=''.join(full[1:len(full)]).lower()
            brand.append(brandname)
            model.append(modelname)
            # استخراج کارکرد به عدد اینتجر و حذف کلمه مایل
            fullmile=mileall[page][num].text
            strmile=fullmile.split(' ')[0]
            strmile=strmile.split(',')
            intmile=int(''.join(strmile))
            mile.append(intmile)
            #استخراج سال به عدد اینتجر
            year.append(int(yearall[page][num].text))
            #استخراج قیمت به عدد اینتجر و حذف کاراکتر دلار
            fullprice=re.findall('^\$(.+)',priceall[page][num].text)
            strprice=fullprice[0].split(',')
            intprice=int(''.join(strprice))
            price.append(intprice)
#همه لیست های نهایی دارای طول برابر می باشند (تست شده) 
#ساخت متغیری که دارای تعداد ماشین ها است
numberof_cars=len(brand)
        

#چک کردن ماشین های اضافه شده در لیست های نهایی
#carnum=0
#for pages in range(0,20):
    #for num in range(0,len(fullname[pages])):
        #print('brand is :'+brand[carnum])
        #print('model is :'+model[carnum])
       # print('year is :'+str(year[carnum]))
        #print('mile is :'+str(mile[carnum]))
        #print('price is :'+str(price[carnum]))
       # carnum+=1
        #print('.\n.\n.\n')
#print(carnum)

#لطفا قبل از ران کردن برنامه دیتابیسی با نام دلخواه بسازید که به شکل زیر متغیر بگیرد
#CREATE TABLE info (brand VARCHAR(100),model VARCHAR(100),year VARCHAR(100),mileage VARCHAR(100),price VARCHAR(100))
#دسترسی به دیتابیسی که کاربر وارد کرده
polesql=mysql.connector.connect(host=clientHOST,user=clientUSER,password=clientPASS,database=clientDATABASE)
executer=polesql.cursor()
#دسترسی به دیتای از قبل ذخیره شده در دیتابیس
#توجه!
#هدف از این کار جلوگیری از ذخیره شدن دیتای تکراری می باشد
#لذا برای این کار تنها دسترسی و جستجوی سه پارامتر برند ، مدل و کارکرد کافی می باشد
savedbrands=[]
savedmodels=[]
savedmiles=[]
#ساخت لیست از موارد خواسته شده
#ساخت لیست برندها
executer.execute('SELECT brand FROM '+clientdatabaseTABLE)
brandtoup=executer.fetchall()
for i in range(len(brandtoup)):
    savedbrands.append(brandtoup[i][0])
#ساخت لیست مدل ها
executer.execute('SELECT model FROM '+clientdatabaseTABLE)
modeltoup=executer.fetchall()
for i in range(len(modeltoup)):
    savedmodels.append(modeltoup[i][0])
#ساخت لیست کارکرد ها
executer.execute('SELECT mileage FROM '+clientdatabaseTABLE)
miletoup=executer.fetchall()
for i in range(len(miletoup)):
    savedmiles.append(miletoup[i][0])

carnumber=0 #شمارشگر ماشین های سیو شده

#ذخیره اطلاعات دریافت شده در دیتابیس
for num in range(numberof_cars):
    #اگر دیتا در دیتابیس نبود آن را ذخیره میکند
    #اگر دیتا تکراری بود آن دیتا و دیتاهای پس از آنرا نیز ذخیره نمیکند و از حلقه بیرون میرود
    if (brand[num] in savedbrands) and (model[num] in savedmodels) and (str(mile[num]) in savedmiles):
        print('saved car found!')
        break
    else:
        query='INSERT INTO '+clientdatabaseTABLE+' (brand,model,year,mileage,price) VALUES(%s,%s,%s,%s,%s)'
        vals=(brand[num],model[num],str(year[num]),str(mile[num]),str(price[num]))
        executer.execute(query,vals)
        polesql.commit()
        carnumber+=1
#چاپ تعداد ماشین های غیرتکراری سیو شده
print('job is done!! the number of new saved cars is : %i'%carnumber)
#پایان

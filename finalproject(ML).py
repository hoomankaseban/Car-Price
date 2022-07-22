#Author:Mr.Programmer
#Part 2
#طبق خواسته استاد پروژه در دو اسکریپت نوشته شد
#*******************************اسکریپت ماشین لرنینگ*******************************
#در این پروژه به خاطر راحتی کاربر و ساخته نشدن مجدد دیتابیس ها در این قسمت نیز نام برند و مدل خواسته میشود
#به خاطر اینکه اگر یکبار قبلا در یک دیتابیسی دیتای ماشین با برند و مدل دیگری ذخیره شده بود مشکلی ایجاد نشود و بشود در همان دیتابیس  
#ماشین های مورد نظر را انتخاب کرد
#پس اگر شما چندبار اسکریپت اول را ران کرده باشید و برند ها و مدل های مختلف ماشین ها در آن ذخیره شده باشند
#مشکلی پیش نمی آید و می توانید در اینجا برند و مدل مورد نظر خود را در همان دیتابیس پیدا کنید
import mysql.connector
from sklearn import tree,preprocessing
#دسترسی به اطلاعات سیستمی و دیتابیسی کاربر
clientHOST=input('please enter your host : ')
clientUSER=input('please enter your user : ')
clientPASS=input('please enter your password : ')
clientDATABASE=input('please enter your database : ')
clientdatabaseTABLE=input('please enter your databaseTABLE : ')
#ساخت پل ارتباطی با دیتابیس
polesql=mysql.connector.connect(host=clientHOST ,user=clientUSER, password=clientPASS, database=clientDATABASE)
executer=polesql.cursor()
#دریافت اطلاعات برند و مدل ماشین مورد نظر
brnd=input('Please insert Your WantedCar BRAND in lowecase (for example:\'bmw\') : ')
#وارد کردن نام مدل ماشین
#توجه کنید در اسکریپت اول چون میخواستیم به آدرس دسترسی پیدا کنیم مشابه آدرس سایت عمل میکردیم
#مثلا بی ام و سری هفت در آدرس سایت 
#7-series 
#نوشته می شد و در اسکریپت اول هم اینگونه خواسته میشد
#ولی در این اسکریپت فقط نام مدل با حروف کوچک بدون فاصله و خط تیره خواسته میشود
#برای اطمینان میتوانید به قسمت نام مدل ماشین رجوع کنید
mdl=input('Please insert Your WantedCar MODEL in lowecase without space and \'-\' (for example:\'7series\') : ')
brands=[]
models=[]
miles=[]
years=[]
prices=[]
#ساخت لیست کارکرد ها
executer.execute('SELECT mileage FROM '+clientdatabaseTABLE+' WHERE brand=\''+brnd+'\''+' AND model=\''+mdl+'\'')
miletoup=executer.fetchall()
for i in range(len(miletoup)):
    miles.append(miletoup[i][0])
#ساخت لیست سال ساخت
executer.execute('SELECT year FROM '+clientdatabaseTABLE+' WHERE brand=\''+brnd+'\''+' AND model=\''+mdl+'\'')
yeartoup=executer.fetchall()
for i in range(len(yeartoup)):
    years.append(yeartoup[i][0])
#ساخت لیست قیمت
executer.execute('SELECT price FROM '+clientdatabaseTABLE+' WHERE brand=\''+brnd+'\''+' AND model=\''+mdl+'\'')
pricetoup=executer.fetchall()
for i in range(len(pricetoup)):
    prices.append(pricetoup[i][0])
#ورودی
x=[]
#خروجی
y=[]
#ریختن ورودی ها در ایکس و قیمت در ایگرگ
for num in range(len(years)):
    m=[]
    m.append(years[num])
    m.append(miles[num])
    x.append(m)
    y.append(prices[num])
#یادگیری ماشین
learner = tree.DecisionTreeClassifier()
learner= learner.fit(x,y)
#دریافت اطلاعات سال و کارکرد ماشین شما
wantedcar_year=input('please enter Production Year of YourCar :  ')
wantedcar_mileage=input('please enter Mileage of YourCar :  ')
#ریختن اطلاعات ماشین کاربر در لیست 
wanted=[[wantedcar_year,wantedcar_mileage]]
#درخواست قیمت خودرو با توجه به اطلاعات وارد شده از برنامه
ans=learner.predict(wanted)
#چاپ قیمت
print('Your car costs about $%s'%ans[0])
#پایان!

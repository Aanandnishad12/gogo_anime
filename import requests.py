import requests
from bs4 import BeautifulSoup
import mysql.connector


mydb = mysql.connector.connect(
host="localhost",
user="root",
password="Anishad@123",
database="bosspet"
)
mycursor = mydb.cursor()
mycursor.execute("""CREATE TABLE if not exists `anime`(
    `id` int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `category` varchar(250) NOT NULL
)ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8""")
# mycursor.execute("ALTER TABLE andi.`bosspetedge_categories` CONVERT TO CHARACTER SET utf8")
x = requests.get("https://gogoanime.fi/")
soup = BeautifulSoup(x.content,"lxml")
for i in range(len(soup.find_all("a")))[21:]:
    if soup.find_all("a")[i].get("href"):
        gnere = "https://gogoanime.fi/"+soup.find_all("a")[i].get("href")
        flag = True
        c = 1
        while flag:
            try:
                hello = requests.get(f"{gnere}?page={c}")
                soup1 = BeautifulSoup(hello.content,"lxml")
                movie = soup1.find("div",class_="last_episodes")
                for i in range(len(movie.find_all("a"))):
                    vinay = "https://gogoanime.fi/"+movie.find_all("a")[i].get("href")  
                    mycursor = mydb.cursor()     
                    mycursor.execute("SELECT id FROM `anime` WHERE `category` = %s", (vinay,))
                    myresult = mycursor.fetchall()
                    # print(myresult)
                    if myresult ==[]:
                        sql = "INSERT INTO  `anime` (category) VALUES('"+vinay+"')"
                        mycursor.execute(sql)
                        mydb.commit()
                    
                c+=1
                print(c)
            except Exception as E:
                print(E)
                flag = False

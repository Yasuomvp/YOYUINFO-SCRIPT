import json
# -*- coding: utf-8 -*-
from configparser import ConfigParser

conf = ConfigParser()
conf.read("db.ini")

host = conf.get("mysql", "host")
username = conf.get("mysql", "username")
password = conf.get("mysql", "password")
db = conf.get("mysql", "db")



import requests
import mysql.connector

if __name__ == '__main__':


    print(host+' '+username+" "+password+" "+db)

    conn = mysql.connector.connect(

        host=host,
        user=username,
        passwd=password,
        db=db

    )

    cursor = conn.cursor()

    games = requests.get('https://www.freetogame.com/api/games')
    jsonStr = games.text[1:-1]
    formatJsonStr = jsonStr.replace('},','}|')
    jsonlist = formatJsonStr.split('|')
    for jsoninfo in jsonlist:

        j = json.loads(jsoninfo)

        title = (""+j["title"]).replace("'","\\'")
        short_description = (""+j["short_description"]).replace("'","\\'")
        publisher = (""+j["publisher"]).replace("'","\\'")
        developer = (""+j["developer"]).replace("'","\\'")

        sql = f'insert into games values({j["id"]},\'{title}\',\'{j["thumbnail"]}\',\'{short_description}\',\'{j["game_url"]}\',\'{j["genre"]}\',\'{j["platform"]}\',\'{publisher}\',\'{developer}\',\'{j["release_date"]}\',\'{j["freetogame_profile_url"]}\');'
        cursor.execute(sql)
        print(j["title"]+" 执行成功")

    conn.commit()
# -*- coding:utf-8 -*-
import json
import sqlite3
from requests import get
from xml.etree.ElementTree import fromstring
from time import sleep
import sys

def printProgress(res):
    sys.stdout.write("\rProgress : {0} %".format(res))
    sys.stdout.flush()

JSON_FILE = "2018Feb22snow.json"
DB_FILE = "data.sqlite3"

report = json.load(open(JSON_FILE))
conn = sqlite3.connect(DB_FILE)

report = report["report"]

c = conn.cursor()
try:
    c.execute('CREATE TABLE report(id integer primary key autoincrement, img_file text, location_id integer, comment text)')
    c.execute('CREATE TABLE location(id integer primary key autoincrement, location text unique, long real, lat real)')
except sqlite3.OperationalError:
    pass

conn.commit()

# まずlocationの処理
print("Setting Location...")
count = 0
for report_data in report.values():
    try:
        count = count + 1
        
        printProgress(str(round(count / len(report) * 100, 2)))
    

        c.execute("select count(*) from location where location = '{0}'".format(report_data['location']))
        location_count = c.fetchall()

        # 登録されてるのが0の場合
        if location_count[0][0] == 0:
            print(report_data['location'])
            res = get("http://www.geocoding.jp/api/", params={"q": report_data['location']})
            xml = fromstring(res.text)
            lat = xml[2][0].text
            long = xml[2][1].text
            insert_location = [report_data['location'], long, lat]
            c.execute('insert into location(location, long, lat) values (?,?,?)', insert_location)
            conn.commit()
            sleep(5)
        else:
            pass
    except KeyboardInterrupt:
        c.close()
        exit()
    except IndexError:
        print("見つからなかったのでパス...")
        pass
    except xml.etree.ElementTree.ParseError:
        print("なにか起きたみたい...")
        pass

# 次にreport処理
print("Setting Report...")
count = 0
for report_data in report.values():
    try:
        count = count + 1
        
        printProgress(str(round(count / len(report) * 100, 2)))

        c.execute("select id from location where location = '{0}'".format(report_data['location']))
        location_count = c.fetchall()

        insert_data = [report_data['img_file'], location_count[0][0], report_data['comment']]
        c.execute('insert into report(img_file, location_id, comment) values (?,?,?)', insert_data)
    except KeyboardInterrupt:
        conn.rollback()
        c.close()
        exit()
    except:
        pass

conn.commit()
c.close()
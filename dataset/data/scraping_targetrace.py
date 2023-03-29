'''
今週のレース情報からレース結果とレース時の馬の情報を取得するスクレイピングコード
'''

import set_url
import open_chrome
import columns

import pandas as pd

from selenium import webdriver
from selenium.webdriver.support.ui import Select,WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup

import os
import time
import requests

#保存先のディレクトリ
dir = 'takamatsu/targetracepage'

def html():
    URL = set_url.horse_target()
    driver,wait = open_chrome.open_chrome(URL)

    HTML_DIR = "html/"+dir
    if not os.path.isdir(HTML_DIR):
        os.makedirs(HTML_DIR)

    url = driver.current_url
    race_id = url.split("=")[1].split("&")[0]
    # list = url.split("/")
    # race_id = list[-1]
    save_file_path = HTML_DIR+"/"+race_id+'.html'

    response = requests.get(url)
    response.encoding = response.apparent_encoding
    html = response.text
    time.sleep(5)
    with open(save_file_path, 'w') as file:
        file.write(html)

    return HTML_DIR

#HTMLデータからスクレイピングする関数を定義
def get_race_html(race_id, html):
    race_list = [race_id]
    horse_list_list = []
    soup = BeautifulSoup(html, 'html.parser')

    # race基本情報
    race_list.append(soup.find("span", class_="RaceNum").get_text())
    race_list.append(soup.find("div", class_="RaceName").get_text())
    RaceData01 = soup.find("div", class_="RaceData01").get_text()
    race_list.append(RaceData01.split("/")[0])
    race_list.append(RaceData01.split("/")[1])
    try:
        race_list.append(RaceData01.split("/")[2])
    except AttributeError:
        race_list.append(None)
    try:
        race_list.append(RaceData01.split("/")[3])
    except AttributeError:
        race_list.append(None)
        
    RaceData02 = soup.find("div", class_="RaceData02").get_text() 
    #RaceData02.split("\n")[0]#->''
    #race_list.append(RaceData02.split("\n")[1])#->'2回'
    race_list.append(RaceData02.split("\n")[2])#->'中京'
    #race_list.append(RaceData02.split("\n")[3])#->'6日目'
    #race_list.append(RaceData02.split("\n")[4])#->'サラ系４歳以上'
    #race_list.append(RaceData02.split("\n")[5])#->'オープン'
    #RaceData02.split("\n")[6]#->'\xa0\xa0\xa0\xa0\xa0'
    #race_list.append(RaceData02.split("\n")[7])#->'(国際)(指)'
    #race_list.append(RaceData02.split("\n")[8])#->'定量'
    race_list.append(RaceData02.split("\n")[9])#->'18頭'
    #RaceData02.split("\n")[10]#->''
    #race_list.append(RaceData02.split("\n")[11])#->'本賞金:17000,6800,4300,2600,1700万円'
    #RaceData02.split("\n")[12]#->''



    
    #tableの情報を取得
    horse_tables = soup.findAll("table", class_="RaceTable01")
    horse_table = horse_tables[0].findAll('tr', class_="HorseList")
    #tableの情報から各情報を抜き出す
    for i in range(len(horse_table)):
        horse_list = [race_id]
        result_row = horse_table[i].findAll("td")
        horse_list.append(result_row[0].get_text())#枠
        horse_list.append(result_row[1].get_text())#番号
        horse_list.append(result_row[3].find('a').get('href').split("/")[-1])#馬ID
        horse_list.append(result_row[4].get_text())#性別年齢
        horse_list.append(result_row[5].get_text())#斤量
        horse_list.append(result_row[6].find('a').get('href').split("/")[-2])#騎手
        horse_list.append(result_row[7].find('a').get('href').split("/")[-2])#厩舎
        try:
            horse_list.append(result_row[8].get_text())#馬体重
        except AttributeError:
            horse_list.append(None) 
        try:
            horse_list.append(result_row[9].get_text())#オッズ
        except AttributeError:
            horse_list.append(None)
        try:
            horse_list.append(result_row[10].get_text())#人気
        except AttributeError:
            horse_list.append(None)
        horse_list.append(result_row[3].get_text())#馬の名前
        horse_list_list.append(horse_list)

    return race_list, horse_list_list


def csv(HTML_DIR):
    #csvの保存場所を設定
    CSV_DIR = "csv/"+dir
    if not os.path.isdir(CSV_DIR):
        os.makedirs(CSV_DIR)
    save_race_csv = CSV_DIR+"/race"+".csv"
    horse_race_csv = CSV_DIR+"/horse"+".csv"

    #上記で定義した関数を使って、各要素をデータフレームに保存
    
    race_df = pd.DataFrame(columns=columns.targetrace_data_columns())
    horse_df = pd.DataFrame(columns=columns.targethorse_data_columns())
    if os.path.isdir(HTML_DIR):
        file_list = os.listdir(HTML_DIR)
        for file_name in file_list:
            with open(HTML_DIR+"/"+file_name, "r") as f:
                html = f.read()
                list = file_name.split(".")
                race_id = list[-2]
                race_list, horse_list_list = get_race_html(race_id, html) 
                for horse_list in horse_list_list:
                    horse_se = pd.Series( horse_list, index=horse_df.columns)
                    horse_df = pd.concat([horse_df, horse_se.to_frame().T], ignore_index=True)
                race_se = pd.Series(race_list, index=race_df.columns )
                race_df = pd.concat([race_df, race_se.to_frame().T], ignore_index=True)

    #dfをcsvに書き出し
    race_df.to_csv(save_race_csv, header=True, index=False)
    horse_df.to_csv(horse_race_csv, header=True, index=False)

if __name__ == '__main__':
    HTML_DIR = html()
    csv(HTML_DIR)
    

'''
過去のレース情報からレース結果とレース時の馬の情報を取得するスクレイピングコード
'''

import set_url
import open_chrome
import columns
import data_cleansing
import upload_cloudstorage

import pandas as pd
import numpy as np

from selenium import webdriver
from selenium.webdriver.support.ui import Select,WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup

import os
import time
import requests
from google.cloud import storage

#保存先のディレクトリ
dir = 'tennosyoharu'
race_date_dict = {}

def html():
    URL = set_url.race_database()
    driver,wait = open_chrome.open_chrome(URL)

    #検索条件の記述
    race_name = "天皇賞(春)"
    year = 2006
    month = 1
    end_year = 2022
    end_month = 12

    #レース名を選択
    race_name_element =driver.find_element(By.CSS_SELECTOR,"#db_search_detail_form > form > table > tbody > tr:nth-child(1) > td > input")
    race_name_element.send_keys(race_name)

    #期間を選択
    year_element =driver.find_element(By.NAME,"start_year")
    year_select = Select(year_element)
    year_select.select_by_value(str(year))
    month_element = driver.find_element(By.NAME,"start_mon")
    month_select = Select(month_element)
    month_select.select_by_value(str(month))
    end_year_element = driver.find_element(By.NAME,"end_year")
    end_year_select = Select(end_year_element)
    end_year_select.select_by_value(str(end_year))
    end_mon_element = driver.find_element(By.NAME,"end_mon")
    end_mon_select = Select(end_mon_element)
    end_mon_select.select_by_value(str(end_month))

    #中央競馬場をチェック
    for i in range(1,11):
        terms = driver.find_element(By.ID,"check_Jyo_"+ str(i).zfill(2))
        terms.click()
    #1札幌　2函館　3福島　4新潟　5東京　6中山　7中京　8京都　9阪神　10小倉　

    #グレードをチェック
    for i in range(1,2):
        terms = driver.find_element(By.ID,"check_grade_"+ str(i))
        terms.click()
    #1:G1　2:G2　3:G3　4:OP　5:3勝(1600万)　6:2勝(1000万)　7:1勝(500万)　8:新馬　9:未勝利　10:未出走　

    # 表示件数を選択(20,50,100の中から最大の100へ)
    list_element = driver.find_element(By.NAME,'list')
    list_select = Select(list_element)
    list_select.select_by_value("100")

    # フォームを送信
    frm = driver.find_element(By.CSS_SELECTOR,"#db_search_detail_form > form")
    frm.submit()
    time.sleep(5)
    wait.until(EC.presence_of_all_elements_located)

    #レースデータをテキストに保存
    TEXT_RACE_DIR = "text/"+dir+"/racepage/"
    if not os.path.isdir(TEXT_RACE_DIR):
        os.makedirs(TEXT_RACE_DIR)

    with open(TEXT_RACE_DIR+"previousrace.txt", mode='w') as f:
        while True:
            time.sleep(5)
            wait.until(EC.presence_of_all_elements_located)
            all_rows = driver.find_element(By.CLASS_NAME,'race_table_01').find_elements(By.TAG_NAME,"tr")
            for row in range(1, len(all_rows)):
                race_href=all_rows[row].find_elements(By.TAG_NAME,"td")[4].find_element(By.TAG_NAME,"a").get_attribute("href")
                f.write(race_href+"\n")
            try:
                target = driver.find_elements(By.LINK_TEXT,"次")[0]
                driver.execute_script("arguments[0].click();", target) 
            except IndexError:
                break


    #テキストデータからHTMLデータに保存
    HTML_RACE_DIR = "html/"+dir+"/racepage/"
    if not os.path.isdir(HTML_RACE_DIR):
        os.makedirs(HTML_RACE_DIR)
            
    with open(TEXT_RACE_DIR+"previousrace.txt", "r") as f:
        urls = f.read().splitlines()
        for url in urls:
            list = url.split("/")
            race_id = list[-2]
            save_file_path = HTML_RACE_DIR+race_id+'.html'
            response = requests.get(url)
            response.encoding = response.apparent_encoding
            html = response.text
            time.sleep(5)
            with open(save_file_path, 'w', encoding='cp932', errors='replace') as file:
                file.write(html)
    return HTML_RACE_DIR

#HTMLデータからスクレイピングする関数を定義
def get_race_html(race_id, html):
    race_list = [race_id]
    horse_list_list = []
    soup = BeautifulSoup(html, 'html.parser')

    # race基本情報
    data_intro = soup.find("div", class_="data_intro")
    race_list.append(data_intro.find("dt").get_text().strip("\n")) # race_round
    race_list.append(data_intro.find("h1").get_text().strip("\n")) # race_title
    race_details1 = data_intro.find("p").get_text().strip("\n").split("\xa0/\xa0")
    race_list.append(race_details1[0]) # race_course
    race_list.append(race_details1[1]) # weather
    race_list.append(race_details1[2]) # ground_status
    race_list.append(race_details1[3]) # time
    race_details2 = data_intro.find("p", class_="smalltxt").get_text().strip("\n").split(" ")
    race_list.append(race_details2[0]) # date
    race_list.append(race_details2[1]) # where_racecourse

    race_date_dict[race_id] = race_details2[0]

    result_rows = soup.find("table", class_="race_table_01 nk_tb_common").findAll('tr') 
    # 上位3着の情報
    race_list.append(len(result_rows)-1) # total_horse_number
    for i in range(1,4):
        row = result_rows[i].findAll('td')
        race_list.append(row[1].get_text()) # frame_number_first or second or third
        race_list.append(row[2].get_text()) # horse_number_first or second or third

    # 払い戻し(単勝・複勝・三連複・3連単)
    pay_back_tables = soup.findAll("table", class_="pay_table_01")

    pay_back1 = pay_back_tables[0].findAll('tr') # 払い戻し1(単勝・複勝)
    race_list.append(pay_back1[0].find("td", class_="txt_r").get_text()) #tansyo
    hukuren = pay_back1[1].find("td", class_="txt_r")
    tmp = []
    for string in hukuren.strings:
        tmp.append(string)
    for i in range(3):
        try:
            race_list.append(tmp[i]) # hukuren_first or second or third
        except IndexError:
            race_list.append("0")

    # 枠連
    try:
        race_list.append(pay_back1[2].find("td", class_="txt_r").get_text())
    except IndexError:
        race_list.append("0")

    # 馬連
    try:
        race_list.append(pay_back1[3].find("td", class_="txt_r").get_text())
    except IndexError:
        race_list.append("0")

    pay_back2 = pay_back_tables[1].findAll('tr') # 払い戻し2(三連複・3連単)

    # wide 1&2
    wide = pay_back2[0].find("td", class_="txt_r")
    tmp = []
    for string in wide.strings:
        tmp.append(string)
    for i in range(3):
        try:
            race_list.append(tmp[i]) # hukuren_first or second or third
        except IndexError:
            race_list.append("0")

    # umatan
    race_list.append(pay_back2[1].find("td", class_="txt_r").get_text()) #umatan

    race_list.append(pay_back2[2].find("td", class_="txt_r").get_text()) #renhuku3
    try:
        race_list.append(pay_back2[3].find("td", class_="txt_r").get_text()) #rentan3
    except IndexError:
        race_list.append("0")

    # horse data
    for rank in range(1, len(result_rows)):
        horse_list = [race_id]
        result_row = result_rows[rank].findAll("td")
        # rank
        horse_list.append(result_row[0].get_text())
        # frame_number
        horse_list.append(result_row[1].get_text())
        # horse_number
        horse_list.append(result_row[2].get_text())
        # horse_id
        horse_list.append(str(result_row[3].find('a').get('href').split("/")[-2]))
        # sex_and_age
        horse_list.append(result_row[4].get_text())
        # burden_weight
        horse_list.append(result_row[5].get_text())
        # rider_id
        horse_list.append(str(result_row[6].find('a').get('href').split("/")[-2]))
        # goal_time
        horse_list.append(result_row[7].get_text())
        # goal_time_dif
        horse_list.append(result_row[8].get_text())
        # time_value(premium)
        horse_list.append(result_row[9].get_text())
        # half_way_rank
        horse_list.append(result_row[10].get_text())
        # last_time(上り)
        horse_list.append(result_row[11].get_text())
        # odds
        horse_list.append(result_row[12].get_text())
        # popular
        horse_list.append(result_row[13].get_text())
        # horse_weight
        horse_list.append(result_row[14].get_text())
        # tame_time(premium)
        horse_list.append(result_row[15].get_text())
        # 16:コメント、17:備考
        # tamer_id
        horse_list.append(str(result_row[18].find('a').get('href').split("/")[-2]))
        # owner_id
        horse_list.append(str(result_row[19].find('a').get('href').split("/")[-2]))

        horse_list_list.append(horse_list)

    horse_href_list=[]
    for row in range(1, len(result_rows)):
        result_row=result_rows[row]
        result_data = result_row.findAll('td')[3]
        horse_href_list.append("https://db.netkeiba.com"+result_data.find('a').get('href'))        

    HTML_HORSE_DIR = "html/"+dir+"/horsepage/"
    if not os.path.isdir(HTML_HORSE_DIR):
        os.makedirs(HTML_HORSE_DIR)   

    for url in horse_href_list:
        list = url.split("/")
        horse_id = list[-2]
        save_file_path = HTML_HORSE_DIR+"-"+race_id+"-"+horse_id+"-"+'.html'
        response = requests.get(url)
        response.encoding = response.apparent_encoding
        html = response.text
        time.sleep(5)
        with open(save_file_path, 'w', encoding='cp932', errors='replace') as file:
            file.write(html)

    return race_list, horse_list_list, HTML_HORSE_DIR

def get_horse_html(horse_id, race_id, html):
    horse_list = [horse_id]
    horse_race_list = []
    soup = BeautifulSoup(html, 'html.parser')
    horse_tables = soup.find("table", class_="db_prof_table")
    horse_table = horse_tables.findAll("td")
    #for i in range(10):
    horse_list.append(horse_table[0].get_text())
    horse_list.append(horse_table[1].find('a').get('href').split("/")[-2])
    horse_list.append(horse_table[2].find('a').get('href').split("/")[-2])
    try:
        horse_list.append(horse_table[3].find('a').get('href').split("/")[-2])
    except:
        horse_list.append(None)
    horse_list.append(horse_table[4].get_text())
    horse_list.append(horse_table[5].get_text())
    horse_list.append(horse_table[6].get_text())
    horse_list.append(horse_table[7].get_text())
    horse_list.append(horse_table[8].find('a').get('href').split("/")[-2])
    
    # horse_table[8]からすべてのリンクのURLの一部を取得する
    url_parts = [link.get('href').split("/")[-2] for link in horse_table[9].find_all('a')]

    # url_partsの要素数が2未満の場合、残りの要素をNaNで埋める
    while len(url_parts) < 2:
        url_parts.append("NaN")

    # horse_listにurl_partsを追加する
    horse_list.extend(url_parts)
    
    #horse_list.append(horse_table[9].get_text())
    blood_tables = soup.find("table", class_="blood_table")
    blood_table = blood_tables.findAll("td")
    #for i in range(6):
    horse_list.append(blood_table[0].find('a').get('href').split("/")[-2])
    horse_list.append(blood_table[1].find('a').get('href').split("/")[-2])
    horse_list.append(blood_table[2].find('a').get('href').split("/")[-2])
    horse_list.append(blood_table[3].find('a').get('href').split("/")[-2])
    horse_list.append(blood_table[4].find('a').get('href').split("/")[-2])
    horse_list.append(blood_table[5].find('a').get('href').split("/")[-2])    
  
    
#horse_race
    horse_race_tmp_df = pd.DataFrame()

    horse_tables = soup.find("table", class_="db_h_race_results")
    horse_trs = horse_tables.findAll("tr")
    for index, horse_tr in enumerate(horse_trs):
        if index == 0:
            continue
        horse_race_list = []
        horse_ra_se = pd.Series(dtype='str')

        horse_tds = horse_tr.findAll("td")
        horse_race_list.append(horse_tds[0].get_text())
        horse_race_list.append(horse_tds[1].get_text())
        horse_race_list.append(horse_tds[2].get_text())
        horse_race_list.append(horse_tds[3].get_text())
        horse_race_list.append(horse_tds[4].get_text())
        horse_race_list.append(horse_tds[4].find('a').get('href').split("/")[-2])
        horse_race_list.append(horse_tds[6].get_text())
        horse_race_list.append(horse_tds[7].get_text())
        horse_race_list.append(horse_tds[8].get_text())
        horse_race_list.append(horse_tds[9].get_text())
        horse_race_list.append(horse_tds[10].get_text())
        horse_race_list.append(horse_tds[11].get_text())
        try:
            horse_race_list.append(horse_tds[12].find('a').get('href').split("/")[-2])
        except AttributeError:
            horse_race_list.append(None)
        horse_race_list.append(horse_tds[13].get_text())
        horse_race_list.append(horse_tds[14].get_text())
        horse_race_list.append(horse_tds[15].get_text())
        horse_race_list.append(horse_tds[17].get_text())
        horse_race_list.append(horse_tds[18].get_text())
        horse_race_list.append(horse_tds[20].get_text())
        horse_race_list.append(horse_tds[21].get_text())
        horse_race_list.append(horse_tds[22].get_text())
        horse_race_list.append(horse_tds[23].get_text())
        try:
            horse_race_list.append(horse_tds[26].find('a').get('href').split("/")[-2])
        except AttributeError:
            horse_race_list.append(None)
        horse_race_list.append(horse_tds[27].get_text())
        horse_ra_se = pd.Series(horse_race_list, index=columns.horse_race_columns(),dtype='str')###
        horse_race_tmp_df = pd.concat([horse_race_tmp_df, horse_ra_se.to_frame().T], ignore_index=True)
#     horse_race_tmp_df = pd.DataFrame(horse_race_list, columns=horse_race_columns)
    horse_race_tmp_df.loc[:, 'horse_id'] = horse_id
    horse_race_tmp_df.loc[:, 'target_race_id'] = race_id
    
    return horse_list , horse_race_tmp_df

def csv(HTML_RACE_DIR):
    #csvの保存場所を設定
    CSV_RACE_DIR = "csv/"+dir+"/racepage/"
    if not os.path.isdir(CSV_RACE_DIR):
        os.makedirs(CSV_RACE_DIR)
    race_csv = CSV_RACE_DIR+"race"+".csv"
    horse_csv = CSV_RACE_DIR+"horse"+".csv"

    #上記で定義した関数を使って、各要素をデータフレームに保存
    
    race_df = pd.DataFrame(columns=columns.race_data_columns())
    horse_df = pd.DataFrame(columns=columns.horse_data_columns())
    if os.path.isdir(HTML_RACE_DIR):
        file_list = os.listdir(HTML_RACE_DIR)
        for file_name in file_list:
            with open(HTML_RACE_DIR+file_name, "r") as f:
                html = f.read()
                list = file_name.split(".")
                race_id = list[-2]
                race_list, horse_list_list, HTML_HORSE_DIR = get_race_html(race_id, html) 
                for horse_list in horse_list_list:
                    horse_se = pd.Series(horse_list, index=horse_df.columns)
                    horse_df = pd.concat([horse_df, horse_se.to_frame().T], ignore_index=True)
                race_se = pd.Series(race_list, index=race_df.columns )
                race_df = pd.concat([race_df, race_se.to_frame().T], ignore_index=True)
    #dfをcsvに書き出し
    race_df.to_csv(race_csv, header=True, index=False)
    horse_df.to_csv(horse_csv, header=True, index=False)

    # CSV_RACE_DIR = CSV_RACE_DIR + "race.csv"
    # CSV_HORSE_DIR = CSV_RACE_DIR + "horse.csv"
    
    CSV_HORSE_DIR = "csv/"+dir+"/horsepage/"
    if not os.path.isdir(CSV_HORSE_DIR):
        os.makedirs(CSV_HORSE_DIR)
    horse_info_csv = CSV_HORSE_DIR+"horse-info.csv"
    horse_race_csv = CSV_HORSE_DIR+"horse-race.csv"
    horse_info_df = pd.DataFrame(columns=columns.horse_info_columns())
    horse_race_df = pd.DataFrame()
        
    if os.path.isdir(HTML_HORSE_DIR):
        file_list = os.listdir(HTML_HORSE_DIR)
        for file_name in file_list:
            with open(HTML_HORSE_DIR+file_name, "r") as f:
                html = f.read()
                list = file_name.split("-")
                horse_id = list[-2]
                race_id = list[-3]
                horse_list , horse_race_tmp_df = get_horse_html(horse_id, race_id, html) 
                horse_se = pd.Series(horse_list, index=horse_info_df.columns)
                horse_info_df = pd.concat([horse_info_df, horse_se.to_frame().T], ignore_index=True)
                horse_race_df = pd.concat([horse_race_df, horse_race_tmp_df], axis=0, ignore_index=True)
    #dfをcsvに書き出し
    horse_info_df.to_csv(horse_info_csv, header=True, index=False)
    horse_race_df.to_csv(horse_race_csv, header=True, index=False)

    return race_df, horse_df, horse_info_df, horse_race_df


if __name__ == '__main__':
    HTML_RACE_DIR = html()
    race_df, horse_df, horse_info_df, horse_race_df = csv(HTML_RACE_DIR)

    #data_cleansing
    #race_df
    race_df = data_cleansing.race_round(race_df)
    race_df = data_cleansing.race_title(race_df)
    race_df = data_cleansing.race_course(race_df)
    race_df = data_cleansing.is_obstacle(race_df)
    race_df = data_cleansing.ground_type(race_df)
    race_df = data_cleansing.is_left_right_straight(race_df)
    race_df = data_cleansing.distance(race_df)
    race_df = data_cleansing.weather(race_df)
    race_df = data_cleansing.ground_status(race_df)
    race_df = data_cleansing.time(race_df)
    race_df = data_cleansing.where_racecourse(race_df)
    race_df = data_cleansing.total_horse_number(race_df)
    race_df = data_cleansing.frame_number_first(race_df)
    race_df = data_cleansing.horse_number_first(race_df)
    race_df = data_cleansing.frame_number_second(race_df)
    race_df = data_cleansing.horse_number_second(race_df)
    race_df = data_cleansing.frame_number_third(race_df)
    race_df = data_cleansing.horse_number_third(race_df)
    race_df = data_cleansing.money(race_df)

    #horse_df
    horse_df = data_cleansing.rank(horse_df)
    horse_df = data_cleansing.frame_number(horse_df)
    horse_df = data_cleansing.horse_number(horse_df)
    horse_df = data_cleansing.burden_weight(horse_df)    
    horse_df = data_cleansing.sex_and_age(horse_df)
    horse_df = data_cleansing.rider_id(horse_df)
    horse_df = data_cleansing.goal_time(horse_df)
    horse_df = data_cleansing.goal_time_dif(horse_df)
    horse_df = data_cleansing.last_time(horse_df)
    horse_df = data_cleansing.odds(horse_df)
    horse_df = data_cleansing.popular(horse_df)
    horse_df = data_cleansing.tame_time(horse_df)
    horse_df = data_cleansing.half_way_rank(horse_df)
    horse_df = data_cleansing.horse_weight(horse_df)
    horse_df = data_cleansing.tamer_id(horse_df)
    horse_df = data_cleansing.owner_id(horse_df)
    horse_df = data_cleansing.burden_weight_rate(horse_df)
    horse_df = data_cleansing.avg_velocity(horse_df, race_df)
    
    #horse_info_df
    horse_info_df = data_cleansing.bday(horse_info_df)
    horse_info_df = data_cleansing.tamer_id(horse_info_df)
    horse_info_df = data_cleansing.owner_id(horse_info_df)
    horse_info_df = data_cleansing.producer_id(horse_info_df)
    horse_info_df = data_cleansing.production_area(horse_info_df)
    horse_info_df = data_cleansing.auction_price(horse_info_df)
    horse_info_df = data_cleansing.winnings(horse_info_df)
    horse_info_df = data_cleansing.lifetime_record(horse_info_df)
    horse_info_df = data_cleansing.inbreeding_1(horse_info_df)
    horse_info_df = data_cleansing.inbreeding_2(horse_info_df)
    horse_info_df = data_cleansing.father(horse_info_df)
    horse_info_df = data_cleansing.faths_father(horse_info_df)
    horse_info_df = data_cleansing.faths_mother(horse_info_df)
    horse_info_df = data_cleansing.mother(horse_info_df)
    horse_info_df = data_cleansing.moths_father(horse_info_df)
    horse_info_df = data_cleansing.moths_mother(horse_info_df)
###今回は断念
    horse_info_df = horse_info_df.drop(['auction_price','winnings'],axis=1)

    #horse_race_df
    horse_race_df = data_cleansing.where_racecourse(horse_race_df)
    horse_race_df = data_cleansing.weather(horse_race_df)
    horse_race_df = data_cleansing.race_round(horse_race_df)
    horse_race_df = data_cleansing.race_title(horse_race_df)
    horse_race_df = data_cleansing.total_horse_number(horse_race_df)
    horse_race_df = data_cleansing.frame_number(horse_race_df)
    horse_race_df = data_cleansing.horse_number(horse_race_df)
    horse_race_df = data_cleansing.horse_weight(horse_race_df)
    horse_race_df = data_cleansing.odds(horse_race_df)
    horse_race_df = data_cleansing.popular(horse_race_df)
    horse_race_df = data_cleansing.rank(horse_race_df)
    horse_race_df = data_cleansing.rider_id(horse_race_df)
    horse_race_df = data_cleansing.burden_weight(horse_race_df)
    horse_race_df = data_cleansing.burden_weight_rate(horse_race_df)
    horse_race_df = data_cleansing.race_course(horse_race_df)
    horse_race_df = data_cleansing.is_obstacle(horse_race_df)
    horse_race_df = data_cleansing.ground_type(horse_race_df)
    horse_race_df = data_cleansing.is_left_right_straight(horse_race_df)
    horse_race_df = data_cleansing.distance(horse_race_df)
    horse_race_df = data_cleansing.ground_status(horse_race_df)
    horse_race_df = data_cleansing.goal_time(horse_race_df)
    horse_race_df = data_cleansing.goal_time_dif(horse_race_df)
    horse_race_df = data_cleansing.half_way_rank(horse_race_df)
    horse_race_df = data_cleansing.pace(horse_race_df)
    horse_race_df = data_cleansing.last_time(horse_race_df)
    horse_race_df = data_cleansing.prize(horse_race_df)
    
    horse_race_df = data_cleansing.delete_race(horse_race_df,race_date_dict)

###今回は断念
    horse_race_df = horse_race_df.drop('prize',axis=1)

    print('race_df')
    print(race_df.info())
    print('horse_df')
    print(horse_df.info())
    print('horse_info_df')
    print(horse_info_df.info())
    print('horse_race_df')
    print(horse_race_df.info())


###

    bucket_name = dir + "_csv_upload_bucket"

    # バケットが存在しない場合は新しいバケットを作成する
    storage_client = storage.Client()
    if not storage_client.lookup_bucket(bucket_name):
        upload_cloudstorage.create_bucket(bucket_name)
    
    MAIN_DIR = "main/"+dir+"/"
    if not os.path.isdir(MAIN_DIR):
        os.makedirs(MAIN_DIR)

    RACE_DIR = MAIN_DIR+"race.csv"
    race_df.to_csv(RACE_DIR, header=True, index=False)
    file_upload = "race.csv"
    file_name = RACE_DIR
    upload_cloudstorage.upload(bucket_name, file_upload, file_name)

    HORSE_DIR = MAIN_DIR+"horse.csv"
    horse_df.to_csv(HORSE_DIR, header=True, index=False)
    file_upload = "horse.csv"
    file_name = HORSE_DIR
    upload_cloudstorage.upload(bucket_name, file_upload, file_name)

    HORSE_INFO_DIR = MAIN_DIR+"horse_info.csv"
    horse_info_df.to_csv(HORSE_INFO_DIR, header=True, index=False)
    file_upload = "horse_info.csv"
    file_name = HORSE_INFO_DIR
    upload_cloudstorage.upload(bucket_name, file_upload, file_name)

    HORSE_RACE_DIR = MAIN_DIR+"horse_race.csv"
    horse_race_df.to_csv(HORSE_RACE_DIR, header=True, index=False)
    file_upload = "horse_race.csv"
    file_name = HORSE_RACE_DIR
    upload_cloudstorage.upload(bucket_name, file_upload, file_name)

###


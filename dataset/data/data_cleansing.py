'''データをきれいにするコード'''

import pandas as pd
import numpy as np
from statistics import mean
from datetime import datetime
import re

##########race_df##########
#race_id

#race_round
def race_round(race_df):
    race_df['race_round'] = race_df['race_round'].astype(str).str.strip() #スペースの削除
    race_df['race_round'] = race_df['race_round'].astype(str).replace(u'\xa0', u'') #\xa0ユニコードを変換
    race_df['race_round'] = race_df['race_round'].astype(str).str.replace('R','') #Rの文字を変換
    race_df['race_round'] = race_df['race_round'].replace('',0) #空白を0に変換
    race_df['race_round'] = race_df['race_round'].fillna(0) #NaNを0に変換
    race_df['race_round'] = race_df['race_round'].astype(int) #int型に変換
    race_df = race_df[race_df['race_round'] != 0] #race_roundがないものは使わない
    return race_df

#race_title
def race_title(race_df):
    race_df["race_title"] = race_df["race_title"].str.split().str[0] #空白で区切られた先頭のみを保存
    race_df['race_rank'] = race_df['race_title'].apply(lambda x: re.search(r'\((.*?)\)', x).group(1) if '(' in x else None) #()でかこまれたものをrace_rankに保存、(がない場合はNone
    race_df['race_rank'] = race_df['race_rank'].replace('.*G1.*', 3,regex=True)
    race_df['race_rank'] = race_df['race_rank'].replace('.*G2.*', 2,regex=True)
    race_df['race_rank'] = race_df['race_rank'].replace('.*G3.*', 1,regex=True)
    race_df['race_rank'] = race_df['race_rank'].apply(lambda x: 0 if x not in [1, 2, 3] else x) #1,2,3じゃない場合、0にする
    race_df['race_rank'] = race_df['race_rank'].astype(int)
    return race_df

#race_course
def race_course(race_df):
    #各情報の抜き出し
    obstacle = race_df["race_course"].str.extract('(障)', expand=True)#障害レース
    ground_type = race_df["race_course"].str.extract('(ダ|芝)', expand=True)#ダートor芝レース
    is_left_right_straight = race_df["race_course"].str.extract('(左|右|直線)', expand=True)#右周りor左周り
    distance = race_df["race_course"].str.extract('(\d+)', expand=True)#距離
    #各情報をカラムに変換
    obstacle.columns ={"is_obstacle"}
    ground_type.columns ={"ground_type"}
    is_left_right_straight.columns = {"is_left_right_straight"}
    distance.columns = {"distance"}
    #データフレームに結合
    race_df = pd.concat([race_df, obstacle], axis=1)
    race_df = pd.concat([race_df, ground_type], axis=1)
    race_df = pd.concat([race_df, is_left_right_straight], axis=1)
    race_df = pd.concat([race_df, distance], axis=1)

    #オリジナルの削除
    race_df.drop(['race_course'], axis=1, inplace=True)
    return race_df

#is_obstacle
def is_obstacle(race_df):
    race_df['is_obstacle'] = race_df['is_obstacle'].replace('障', 1)#障を1に、欠損値を0に変換
    race_df['is_obstacle'] = race_df['is_obstacle'].replace(np.nan, 0)
    race_df['is_obstacle'] = race_df['is_obstacle'].astype(int)
    return race_df   

#ground_type
def ground_type(race_df):
    race_df['ground_type'] = race_df['ground_type'].replace('.*(ダ).*', 1,regex=True)
    race_df['ground_type'] = race_df['ground_type'].replace('.*(芝).*', 2,regex=True)
    race_df['ground_type'] = race_df['ground_type'].replace(np.nan, 0)
    race_df['ground_type']  = race_df['ground_type'].astype(int)
    return race_df

#is_left_right_straight
def is_left_right_straight(race_df):
    race_df['is_left_right_straight'] = race_df['is_left_right_straight'].replace('.*(左).*', 1,regex=True)
    race_df['is_left_right_straight'] = race_df['is_left_right_straight'].replace('.*(右).*', 2,regex=True)
    race_df['is_left_right_straight'] = race_df['is_left_right_straight'].replace('.*(直線).*', 0,regex=True)
    race_df['is_left_right_straight'] = race_df['is_left_right_straight'].replace(np.nan, 0)
    race_df['is_left_right_straight']  = race_df['is_left_right_straight'].astype(int)
    return race_df

#distance
def distance(race_df):
    race_df.dropna(subset=['distance'], inplace=True)
    race_df['distance']  = race_df['distance'].astype(int)
    return race_df

#weather
def weather(race_df):
    race_df['weather'] = race_df['weather'].astype(str).replace(u'\xa0', u'')
    race_df['weather'] = race_df['weather'].astype(str).str.strip('天候 :')
    race_df['weather'] = race_df['weather'].replace('.*(晴).*', 1,regex=True)
    race_df['weather'] = race_df['weather'].replace('.*(曇).*', 2,regex=True)
    race_df['weather'] = race_df['weather'].replace('.*(小雨).*', 3,regex=True)
    race_df['weather'] = race_df['weather'].replace('.*(小雪).*', 4,regex=True)
    race_df['weather'] = race_df['weather'].replace('.*(雨).*', 5,regex=True)
    race_df['weather'] = race_df['weather'].replace('.*(雪).*', 6,regex=True)
    race_df['weather'] = race_df['weather'].replace('', np.nan)
    race_df['weather'] = race_df['weather'].replace(np.nan, 0)
    race_df['weather'] = race_df['weather'].astype(int)
    return race_df

#ground_status
def ground_status(race_df):
    race_df['ground_status'] = race_df['ground_status'].replace('.*(不良).*', 4,regex=True)
    race_df['ground_status'] = race_df['ground_status'].replace('.*(稍重).*', 2,regex=True)
    race_df['ground_status'] = race_df['ground_status'].replace('.*(良).*', 1,regex=True)
    race_df['ground_status'] = race_df['ground_status'].replace('.*(稍).*', 2,regex=True)
    race_df['ground_status'] = race_df['ground_status'].replace('.*(重).*', 3,regex=True)
    race_df['ground_status'] = race_df['ground_status'].replace('.*(不).*', 5,regex=True)
    race_df['ground_status'] = race_df['ground_status'].replace('', np.nan)
    race_df['ground_status'] = race_df['ground_status'].replace(np.nan, 0)
    return race_df

#date
def date(race_df):
    race_df["date"] = race_df["date"].str.split().str[0]
    return race_df

#time
def time(race_df):
    race_df["time"] = race_df["time"].str.extract(r"(\d{1,2}:\d{2})") #timeカラムを正規表現で抽出
    race_df["datetime"] = race_df["date"].astype(str) + race_df["time"].astype(str) #timeとdateを結合して、datetimeを作成
    race_df["datetime"] = pd.to_datetime(race_df["datetime"], format='%Y年%m月%d日%H:%M') #datetimeカラムを時間単位に変換 
    race_df["time"] = pd.to_datetime(race_df["time"], format='%H:%M') #timeカラムを時間単位に変換 
    race_df["date"] = pd.to_datetime(race_df["date"], format='%Y年%m月%d日') #dateカラムを時間単位に変換 
    race_df = race_df.drop(['time'],axis=1)
    return race_df


#where_racecourse
def where_racecourse(race_df):
    try:
        race_df["where_racecourse"] = race_df["where_racecourse"].str.replace('\d*回(..)\d*日目', r'\1',regex=True)
    except:
        pass
    try:
        race_df['where_racecourse'] = race_df['where_racecourse'].str.replace('\d+', '',regex=True)
    except:
        pass
    #エンコーディング
    race_df['where_racecourse'] = race_df['where_racecourse'].replace('.*(札幌).*', 1,regex=True)
    race_df['where_racecourse'] = race_df['where_racecourse'].replace('.*(函館).*', 2,regex=True)
    race_df['where_racecourse'] = race_df['where_racecourse'].replace('.*(福島).*', 3,regex=True)
    race_df['where_racecourse'] = race_df['where_racecourse'].replace('.*(新潟).*', 4,regex=True)
    race_df['where_racecourse'] = race_df['where_racecourse'].replace('.*(東京).*', 5,regex=True)
    race_df['where_racecourse'] = race_df['where_racecourse'].replace('.*(中山).*', 6,regex=True)
    race_df['where_racecourse'] = race_df['where_racecourse'].replace('.*(中京).*', 7,regex=True)
    race_df['where_racecourse'] = race_df['where_racecourse'].replace('.*(京都).*', 8,regex=True)
    race_df['where_racecourse'] = race_df['where_racecourse'].replace('.*(阪神).*', 9,regex=True)
    race_df['where_racecourse'] = race_df['where_racecourse'].replace('.*(小倉).*', 10,regex=True)
    race_df["where_racecourse"] = race_df["where_racecourse"].astype(str).apply(lambda x: 0 if not x.isdigit() else x)#数字以外を0に
    race_df['where_racecourse'] = race_df['where_racecourse'].astype(int)
    return race_df

#total_horse_number
def total_horse_number(race_df):
    race_df['total_horse_number'] = race_df['total_horse_number'].replace(u'\xa0', u'')
    race_df['total_horse_number'] = race_df['total_horse_number'].astype(str).str.extract('(\d+)')
    race_df.dropna(subset=['total_horse_number'], inplace=True)
    race_df['total_horse_number'] = race_df['total_horse_number'].astype(int)
    return race_df

#frame_number_first
def frame_number_first(race_df):
    race_df['frame_number_first'] = race_df['frame_number_first'].replace(u'\xa0', u'')
    race_df['frame_number_first'] = race_df['frame_number_first'].astype(int)
    return race_df
#horse_number_first
def horse_number_first(race_df):
    race_df['horse_number_first'] = race_df['horse_number_first'].replace(u'\xa0', u'')
    race_df['horse_number_first'] = race_df['horse_number_first'].astype(int)
    return race_df
#frame_number_second
def frame_number_second(race_df):
    race_df['frame_number_second'] = race_df['frame_number_second'].replace(u'\xa0', u'')
    race_df['frame_number_second'] = race_df['frame_number_second'].astype(int)
    return race_df
#horse_number_second
def horse_number_second(race_df):
    race_df['horse_number_second'] = race_df['horse_number_second'].replace(u'\xa0', u'')
    race_df['horse_number_second'] = race_df['horse_number_second'].astype(int)
    return race_df
#frame_number_third
def frame_number_third(race_df):
    race_df['frame_number_third'] = race_df['frame_number_third'].replace(u'\xa0', u'')
    race_df['frame_number_third'] = race_df['frame_number_third'].astype(int)
    return race_df
#horse_number_third
def horse_number_third(race_df):
    race_df['horse_number_third'] = race_df['horse_number_third'].replace(u'\xa0', u'')
    race_df['horse_number_third'] = race_df['horse_number_third'].astype(int)
    return race_df
#taisyo, hukusyo_first, hukusyo_second, hukusyo_third, wakuren, umaren, wide_1_2, wide_1_3, wide_2_3, umatan, renhuku3, rentan3
def money(race_df):
    race_df['tansyo'] = race_df['tansyo'].astype(str).str.replace(",", "")
    race_df['tansyo'] = race_df['tansyo'].astype(int)
    race_df['hukusyo_first'] = race_df['hukusyo_first'].astype(str).str.replace(",", "")
    race_df['hukusyo_first'] = race_df['hukusyo_first'].astype(int)
    race_df['hukusyo_second'] = race_df['hukusyo_second'].astype(str).str.replace(",", "")
    race_df['hukusyo_second'] = race_df['hukusyo_second'].astype(int)
    race_df['hukusyo_third'] = race_df['hukusyo_third'].astype(str).str.replace(",", "")
    race_df['hukusyo_third'] = race_df['hukusyo_third'].astype(int)
    race_df['wakuren'] = race_df['wakuren'].astype(str).str.replace(",", "")
    race_df['wakuren'] = race_df['wakuren'].astype(int)
    race_df['umaren'] = race_df['umaren'].astype(str).str.replace(",", "")
    race_df['umaren'] = race_df['umaren'].astype(int)
    race_df['wide_1_2'] = race_df['wide_1_2'].astype(str).str.replace(",", "")
    race_df['wide_1_2'] = race_df['wide_1_2'].astype(int)
    race_df['wide_1_3'] = race_df['wide_1_3'].astype(str).str.replace(",", "")
    race_df['wide_1_3'] = race_df['wide_1_3'].astype(int)
    race_df['wide_2_3'] = race_df['wide_2_3'].astype(str).str.replace(",", "")
    race_df['wide_2_3'] = race_df['wide_2_3'].astype(int)
    race_df['umatan'] = race_df['umatan'].astype(str).str.replace(",", "")
    race_df['umatan'] = race_df['umatan'].astype(int)
    race_df['renhuku3'] = race_df['renhuku3'].astype(str).str.replace(",", "")
    race_df['renhuku3'] = race_df['renhuku3'].astype(int)
    race_df['rentan3'] = race_df['rentan3'].astype(str).str.replace(",", "")
    race_df['rentan3'] = race_df['rentan3'].astype(int)
    return race_df

##########horse_df##########
#race_id

#rank
def rank(horse_df):
    #is_downカラムを作成
    is_down = horse_df["rank"].astype(str).str.extract('(\(降\))', expand=True)
    is_down.columns ={"is_down"}
    horse_df = pd.concat([horse_df, is_down], axis=1)
    horse_df.fillna(value={'is_down': 0}, inplace=True)
    horse_df['is_down'] = horse_df['is_down'].replace('(降)', 1)
    ## 余分な文字を削除
    horse_df['rank'] = horse_df['rank'].replace(u'\xa0', u'')
    horse_df['rank'] = horse_df['rank'].apply(lambda x: x.replace("(降)", ""))
    horse_df['rank'] = horse_df['rank'].apply(lambda x: x.replace("(再)", ""))
    horse_df = horse_df[(horse_df['rank'] != "取") & (horse_df['rank'] != "除") & (horse_df['rank'] != "失") & (horse_df['rank'] != "中")]
    horse_df['rank'] = horse_df['rank'].replace('', np.nan)
    horse_df.dropna(subset=['rank'], inplace=True)
    horse_df['rank'] = horse_df['rank'].astype(int)
    return horse_df

#frame_number
def frame_number(horse_df):
    horse_df['frame_number'] = horse_df['frame_number'].replace(u'\xa0', u'')
    horse_df['frame_number'] = horse_df['frame_number'].replace('', 0)
    horse_df['frame_number'] = horse_df['frame_number'].astype(int)
    return horse_df

#horse_number
def horse_number(horse_df):
    horse_df['horse_number'] = horse_df['horse_number'].replace(u'\xa0', u'')
    horse_df['horse_number'] = horse_df['horse_number'].replace('', 0)
    horse_df['horse_number'] = horse_df['horse_number'].astype(int)
    return horse_df

#horse_id

#burden_weight
def burden_weight(horse_df):
    horse_df['burden_weight'] = horse_df['burden_weight'].replace(u'\xa0', u'')
    horse_df['burden_weight'] = horse_df['burden_weight'].replace(np.nan, 0)
    horse_df['burden_weight'] = horse_df['burden_weight'].astype(float)
    return horse_df

#sex_and_age
def sex_and_age(horse_df):
    #age
    horse_df["age"] = horse_df["sex_and_age"].str.extract('([0-9]+)', expand=True)#数字のみ抜き出し
    horse_df["age"] = horse_df["age"] .astype(int)
    #sex
    horse_df["sex_and_age"]  = horse_df["sex_and_age"].replace('.*(牡).*', 0,regex=True)
    horse_df["sex_and_age"]  = horse_df["sex_and_age"].replace('.*(牝).*', 1,regex=True)
    horse_df["sex_and_age"]  = horse_df["sex_and_age"].replace('.*(セ).*', 2,regex=True)
    horse_df["sex"] = horse_df["sex_and_age"]
    horse_df= horse_df.drop('sex_and_age', axis=1)
    return horse_df

#rider_id
def rider_id(horse_df):
    horse_df['rider_id'] = horse_df['rider_id'].replace(u'\xa0', u'')
    horse_df['rider_id'] = horse_df['rider_id'].replace(np.nan, 'NaN')
    return horse_df

#goal_time
def goal_time(horse_df):
    horse_df['goal_time'] = horse_df['goal_time'].replace(u'\xa0', u'')
    horse_df['goal_time'] = horse_df['goal_time'].replace('', np.nan)
    horse_df['goal_time'] = pd.to_datetime(horse_df['goal_time'], format='%M:%S.%f') - pd.to_datetime('00:00.0', format='%M:%S.%f')#00:00.0との差を取得
    horse_df['goal_time'] = horse_df['goal_time'].dt.total_seconds()#取得した差を秒に変換
    #horse_df.fillna(value={'goal_time': horse_df['goal_time'].max()}, inplace=True)#欠損値を最大値で埋める
    #horse_df['goal_time'] = horse_df.groupby('race_id', group_keys=False)['goal_time'].apply(lambda x: x.fillna(x.max()))#欠損値を最大値で埋める
    horse_df.dropna(subset=['goal_time'], inplace=True)
    horse_df['goal_time'] = horse_df['goal_time'].astype(float)
    return horse_df

#goal_time_dif
def goal_time_dif(horse_df):
    horse_df['goal_time_dif'] = horse_df.groupby('race_id', group_keys=False)['goal_time'].diff().reset_index(drop=True)
    horse_df.dropna(subset=['goal_time_dif'],inplace=True)
    horse_df['goal_time_dif'] = horse_df['goal_time_dif'].astype(float)
    return horse_df

#last_time
def last_time(horse_df):
    horse_df['last_time'] = horse_df['last_time'].replace(u'\xa0', u'')
    horse_df['last_time'] = horse_df['last_time'].replace('', np.nan)
    #horse_df.fillna(value={'last_time': horse_df['last_time'].max()}, inplace=True)#欠損値を最大値で埋める
    #horse_df['last_time'] = horse_df.groupby('race_id', group_keys=False)['last_time'].apply(lambda x: x.fillna(x.max()))#欠損値を最大値で埋める
    horse_df.dropna(subset=['last_time'], inplace=True)
    horse_df["last_time"] = horse_df["last_time"].astype(float)
    horse_df["last_time"] = horse_df["last_time"].apply(lambda x: int((x // 100) * 60 + (x % 100) + 0.5))
    return horse_df

#odds
def odds(horse_df):
    horse_df['odds'] = horse_df['odds'].replace(u'\xa0', u'')
    horse_df['odds'] = horse_df['odds'].str.replace('\D', '', regex=True)
    horse_df['odds'] = horse_df['odds'].replace('', 0)
    horse_df['odds'] = horse_df['odds'].astype(int)
    return horse_df

#popular
def popular(horse_df):
    horse_df['popular'] = horse_df['popular'].replace(u'\xa0', u'')
    horse_df['popular'] = horse_df['popular'].str.replace('\D', '', regex=True)
    horse_df['popular'] = horse_df['popular'].replace('', 0)
    horse_df['popular'] = horse_df['popular'].astype(int)
    return horse_df

#time_value
#tame_time
def tame_time(horse_df):
    #time_value, tame_time(プレミアム会員向けの情報なので削除
    horse_df.drop(['time_value'], axis=1, inplace=True)
    horse_df.drop(['tame_time'], axis=1, inplace=True)
    return horse_df

#half_way_rank
def half_way_rank(horse_df):
    horse_df['half_way_rank'] = horse_df['half_way_rank'].replace(u'\xa0', u'')
    horse_df["half_way_rank"] = horse_df["half_way_rank"].replace('', np.nan)
    horse_df["half_way_rank"] = horse_df["half_way_rank"].apply(lambda x: mean([float(n) for n in (x.split("-"))]) if (type(x) is str and len(x) > 0) else float(x))
    #horse_df['half_way_rank'] = horse_df.groupby('race_id', group_keys=False)['half_way_rank'].apply(lambda x: x.fillna(x.max()))
    horse_df.dropna(subset=['half_way_rank'], inplace=True)
    horse_df["half_way_rank"] = horse_df["half_way_rank"].astype(float)
    return horse_df

#horse_weight
def horse_weight(horse_df):
    horse_df['horse_weight'] = horse_df['horse_weight'].replace(u'\xa0', u'')#不要な文字の削除
    horse_df['horse_weight'] = horse_df['horse_weight'].replace('.*計不.*', "", regex=True)
    horse_df["horse_weight"] = horse_df["horse_weight"].replace('', np.nan)
    horse_df['horse_weight_dif'] = horse_df["horse_weight"].astype(str).str.extract('\(([-|+]?\d*)\)', expand=True)#()の文字だけ取得し、horse_weight_difカラムに保存
    horse_df['horse_weight'] = horse_df['horse_weight'].replace('\(([-|+]?\d*)\)', '', regex=True)#()の文字を削除
    horse_df['horse_weight'] = pd.to_numeric(horse_df["horse_weight"], errors="coerce")#可能であれば、数値型に変換
    horse_df['horse_weight_dif'] = horse_df['horse_weight_dif'].astype(str).str.rstrip('+')
    horse_df['horse_weight_dif'] = pd.to_numeric(horse_df["horse_weight_dif"], errors="coerce")#可能であれば、数値型に変換
    # horse_df['horse_weight'] = horse_df.groupby('race_id', group_keys=False)['horse_weight'].apply(lambda x: x.replace(np.nan, x.max()))#欠損値はそのレースの最大値に置換
    # horse_df['horse_weight_dif'] = horse_df.groupby('race_id', group_keys=False)['horse_weight_dif'].apply(lambda x: x.fillna(x.max() if x.notna().any() else x))#欠損値はそのレースの最大値に置換
    return horse_df

#tamer_id
def tamer_id(horse_df):
    horse_df['tamer_id'] = horse_df['tamer_id'].replace(u'\xa0', u'')
    horse_df['tamer_id'] = horse_df['tamer_id'].replace(np.nan, 'NaN')
    return horse_df

#owner_id
def owner_id(horse_df):
    horse_df['owner_id'] = horse_df['owner_id'].replace(u'\xa0', u'')
    horse_df['owner_id'] = horse_df['owner_id'].replace(np.nan, 'NaN')
    return horse_df

#burden_weight_rate
def burden_weight_rate(horse_df):
    horse_df['burden_weight_rate'] = horse_df['burden_weight']/horse_df['horse_weight']
    return horse_df

#avg_velocity
def avg_velocity(horse_df,race_df):
    race_tmp_df = race_df[["race_id", "distance"]]#レース距離情報をmerge
    horse_df = pd.merge(horse_df, race_tmp_df, on='race_id')
    horse_df["avg_velocity"] = horse_df["distance"]/horse_df["goal_time"]
    horse_df.drop(['distance'], axis=1, inplace=True)#distanceの削除
    return horse_df

#horse_name
def horse_name(horse_df):
    horse_df['horse_name'] = horse_df['horse_name'].apply(lambda x: re.sub(r'[^a-zA-Zぁ-んァ-ン一-龥ー]', '', x))
    return horse_df

##########horse_info_df##########
#horse_id

#bday
def bday(horse_info_df):
    horse_info_df["bday"] = pd.to_datetime(horse_info_df["bday"], format='%Y年%m月%d日')
    return horse_info_df

#tame_id

#owner_id

#producer_id
def producer_id(horse_info_df):
    horse_info_df.loc[horse_info_df['producer_id'] == 'owner.netkeiba.com', 'producer_id'] = np.nan #特定の文字の場合欠損値に置換
    horse_info_df['producer_id'] = horse_info_df['producer_id'].replace(np.nan, 'NaN')
    return horse_info_df

#production area
def production_area(horse_info_df):
    horse_info_df['production_area'] = horse_info_df['production_area'].apply(lambda x: x.replace('\n', ''))
    return horse_info_df

#auction price
def auction_price(horse_info_df):
    horse_info_df['auction_price'] = horse_info_df['auction_price'].apply(lambda x: x.replace('\n', ''))
    # horse_info_df["auction_price"] = horse_info_df["auction_price"].str.extract('(\d+([,.]\d+)*)\s*(億|\d+万円)?', expand=True)
    # horse_info_df["auction_price"] = horse_info_df["auction_price"].fillna(0)
    return horse_info_df

#winnings
def winnings(horse_info_df):
    horse_info_df['winnings'] = horse_info_df['winnings'].apply(lambda x: x.replace('\n', ''))
    # horse_info_df["winnings"] = horse_info_df["winnings"].str.extract('(\d+([,.]\d+)*)\s*(億|\d+万円)?', expand=True)
    # horse_info_df["winnings"] = horse_info_df["winnings"].fillna(0)
    return horse_info_df

#lifetime record
def lifetime_record(horse_info_df):
    horse_info_df['lifetime_record'] = horse_info_df['lifetime_record'].apply(lambda x: x.replace('\n', ''))
    return horse_info_df

#wined race title

#inbreeding_1
def inbreeding_1(horse_info_df):
    horse_info_df['inbreeding_1'] = horse_info_df['inbreeding_1'].astype(str)
    horse_info_df['inbreeding_1'] = horse_info_df['inbreeding_1'].replace(np.nan, 'NaN')
    return horse_info_df

#inbreeding_2
def inbreeding_2(horse_info_df):
    horse_info_df['inbreeding_2'] = horse_info_df['inbreeding_2'].astype(str)#.str.rstrip('.0')
    horse_info_df['inbreeding_2'] = horse_info_df['inbreeding_2'].replace(np.nan, 'NaN')
    horse_info_df['inbreeding_2'] = horse_info_df['inbreeding_2'].replace('None', 'NaN')
    return horse_info_df

#father
def father(horse_info_df):
    horse_info_df['father'] = horse_info_df['father'].astype(str)
    horse_info_df['father'] = horse_info_df['father'].replace(np.nan, 'NaN')
    return horse_info_df

#faths_father
def faths_father(horse_info_df):
    horse_info_df['faths_father'] = horse_info_df['faths_father'].astype(str)
    horse_info_df['faths_father'] = horse_info_df['faths_father'].replace(np.nan, 'NaN')
    return horse_info_df

#faths_mother
def faths_mother(horse_info_df):
    horse_info_df['faths_mother'] = horse_info_df['faths_mother'].astype(str)
    horse_info_df['faths_mother'] = horse_info_df['faths_mother'].replace(np.nan, 'NaN')
    return horse_info_df

#mother
def mother(horse_info_df):
    horse_info_df['mother'] = horse_info_df['mother'].astype(str)
    horse_info_df['mother'] = horse_info_df['mother'].replace(np.nan, 'NaN')
    return horse_info_df

#moths_father
def moths_father(horse_info_df):
    horse_info_df['moths_father'] = horse_info_df['moths_father'].astype(str)
    horse_info_df['moths_father'] = horse_info_df['moths_father'].replace(np.nan, 'NaN')
    return horse_info_df

#moths_mother
def moths_mother(horse_info_df):
    horse_info_df['moths_mother'] = horse_info_df['moths_mother'].astype(str)
    horse_info_df['moths_mother'] = horse_info_df['moths_mother'].replace(np.nan, 'NaN')
    return horse_info_df

##########horse_race_df##########
#date
def delete_race(horse_race_df,race_date_dict):
    horse_race_df['date'] = pd.to_datetime(horse_race_df['date'])
    horse_race_df['race_date'] = None
    # レースIDごとに日付を探して、'race_date'カラムに代入する
    for i, row in horse_race_df.iterrows():
        race_id = row['target_race_id']
        race_date = race_date_dict.get(str(race_id))
        horse_race_df.at[i, 'race_date'] = race_date

    horse_race_df["race_date"] = pd.to_datetime(horse_race_df["race_date"], format='%Y年%m月%d日')

    horse_race_df.drop(horse_race_df[horse_race_df['date'] >= horse_race_df['race_date']].index, inplace=True)
    return horse_race_df

#whereracecourse

#weather

#race_round

#race_title

#race_id

#total_horse_number

#frame_number

#horse_number

#odds

#popular

#rank

#rider_id

#burden_weight

#race_course
#distance
# def distance(horse_race_df):
#     horse_race_df['ground_type'] = horse_race_df['distance'].astype(str).str.extract('(芝|ダ)').fillna(0)
#     horse_race_df['distance'] = horse_race_df['distance'].astype(str) .str.extract('(\d+)').fillna(0).astype(int)  
#     return horse_race_df

#groud_status

#goal_time

#goal_time_dif

#half_way_rank

#pace
def pace(horse_race_df):
    horse_race_df['pace'] = horse_race_df['pace'].replace(u'\xa0', u'')
    horse_race_df['pace'] = horse_race_df['pace'].replace('', np.nan)
    horse_race_df["pace"] = horse_race_df["pace"].apply(lambda x: mean([float(n) for n in (x.split("-"))]) if (type(x) is str and len(x) > 0) else float(x))
    #horse_df['pace'] = horse_df.groupby('race_id', group_keys=False)['pace'].apply(lambda x: x.fillna(x.max()))
    horse_race_df.dropna(subset=['pace'], inplace=True)
    return horse_race_df

#last_time

#horse_weight
#上にある

#runner_up_horse_id

#prize
def prize(horse_race_df):
    # horse_race_df["prize"] = horse_race_df["prize"].str.extract('(\d{1,3}(,\d{3})*(\.\d{1,2})?)', expand=True)
    # horse_race_df["prize"] = horse_race_df["prize"].fillna(0)
    return horse_race_df

#horse_id
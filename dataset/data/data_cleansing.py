'''データをきれいにするコード'''

import pandas as pd
import numpy as np
from statistics import mean

# race_df = pd.read_csv("../data/csv/takamatsu/racepage/race.csv")
# horse_df = pd.read_csv("../data/csv/takamatsu/racepage/horse.csv")

##########race_df##########
#race_id

#race_round
def race_round(race_df):
    race_df['race_round'] = race_df['race_round'].str.strip('R \n')
    return race_df

#race_title

#race_course
def race_course(race_df):
    #ストリングデータから各情報の抽出
    #障害レース
    obstacle = race_df["race_course"].str.extract('(障)', expand=True)
    #ダートor芝レース
    ground_type = race_df["race_course"].str.extract('(ダ|芝)', expand=True)
    #右周りor左周り
    is_left_right_straight = race_df["race_course"].str.extract('(左|右|直線)', expand=True)
    #距離
    distance = race_df["race_course"].str.extract('(\d+)m', expand=True)
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
    #右左がないものを直線に変更
    race_df["is_left_right_straight"] = race_df["is_left_right_straight"].fillna("直線")
    #障を1に、欠損値を0に変換
    race_df['is_obstacle'] = race_df['is_obstacle'].replace('障', 1)
    race_df.fillna(value={'is_obstacle': 0}, inplace=True)
    #オリジナルの削除
    race_df.drop(['race_course'], axis=1, inplace=True)
    return race_df

#weather
def weather(race_df):
    race_df['weather'] = race_df['weather'].str.strip('天候 :')
    weather_rain = race_df["weather"].str.extract('(小雨|雨)', expand=True)
    weather_snow = race_df["weather"].str.extract('(小雪|雪)', expand=True)
    weather_rain.columns ={"weather_rain"}
    weather_snow.columns ={"weather_snow"}
    race_df = pd.concat([race_df, weather_rain], axis=1)
    race_df = pd.concat([race_df, weather_snow], axis=1)

    race_df.fillna(value={'weather_rain': 0}, inplace=True)
    race_df['weather_rain'] = race_df['weather_rain'].replace('小雨', 1)
    race_df['weather_rain'] = race_df['weather_rain'].replace('雨', 2)
    race_df.fillna(value={'weather_snow': 0}, inplace=True)
    race_df['weather_snow'] = race_df['weather_snow'].replace('小雪', 1)
    race_df['weather_snow'] = race_df['weather_snow'].replace('雪', 2)
    return race_df

#ground_status
def ground_status(race_df):
    race_df['ground_status'] = race_df['ground_status'].replace('.*(稍重).*', 4,regex=True)
    race_df['ground_status'] = race_df['ground_status'].replace('.*(重).*', 3,regex=True)
    race_df['ground_status'] = race_df['ground_status'].replace('.*(不).*', 3,regex=True)
    race_df['ground_status'] = race_df['ground_status'].replace('.*(不良).*', 2,regex=True)
    race_df['ground_status'] = race_df['ground_status'].replace('.*(良).*', 1,regex=True)
    return race_df


#time
def time(race_df):
    race_df["time"] = race_df["time"].str.replace('発走 : (\d\d):(\d\d)(.|\n)*', r'\1時\2分')
    race_df["datetime"] = race_df["date"] + race_df["time"]
    race_df["datetime"] = pd.to_datetime(race_df['datetime'], format='%Y年%m月%d日%H時%M分')
    return race_df

#date

#where_racecourse
def where_racecourse(race_df):
    race_df["where_racecourse"] = race_df["where_racecourse"].str.replace('\d*回(..)\d*日目', r'\1')
    return race_df

#total_horse_number

#frame_number_first

#horse_number_first

#frame_number_second

#horse_number_second

#frame_number_third

#horse_number_third

#taisyo, hukusyo_first, hukusyo_second, hukusyo_third, wakuren, umaren, wide_1_2, wide_1_3, wide_2_3, umatan, renhuku3, rentan3
def money(race_df):
    race_df['tansyo'] = race_df['tansyo'].apply(lambda x: int(x.replace(",", "")) if type(x) is str else int(x))
    race_df['hukusyo_first'] = race_df['hukusyo_first'].apply(lambda x: int(x.replace(",", "")) if type(x) is str else int(x))
    race_df['hukusyo_second'] = race_df['hukusyo_second'].apply(lambda x: int(x.replace(",", "")) if type(x) is str else int(x))
    race_df['hukusyo_third'] = race_df['hukusyo_third'].apply(lambda x: int(x.replace(",", "")) if type(x) is str else int(x))
    race_df['wakuren'] = race_df['wakuren'].apply(lambda x: int(x.replace(",", "")) if type(x) is str else int(x))
    race_df['umaren'] = race_df['umaren'].apply(lambda x: int(x.replace(",", "")) if type(x) is str else int(x))
    race_df['wide_1_2'] = race_df['wide_1_2'].apply(lambda x: int(x.replace(",", "")) if type(x) is str else int(x))
    race_df['wide_1_3'] = race_df['wide_1_3'].apply(lambda x: int(x.replace(",", "")) if type(x) is str else int(x))
    race_df['wide_2_3'] = race_df['wide_2_3'].apply(lambda x: int(x.replace(",", "")) if type(x) is str else int(x))
    race_df['umatan'] = race_df['umatan'].apply(lambda x: int(x.replace(",", "")) if type(x) is str else int(x))
    race_df['renhuku3'] = race_df['renhuku3'].apply(lambda x: int(x.replace(",", "")) if type(x) is str else int(x))
    race_df['rentan3'] = race_df['rentan3'].apply(lambda x: int(x.replace(",", "")) if type(x) is str else int(x)) 
    return race_df


##########horse_df##########
#race_id

#rank
def rank(horse_df):
    horse_df["rank"] = horse_df["rank"].astype(str)
    is_down = horse_df["rank"].str.extract('(\(降\))', expand=True)
    is_down.columns ={"is_down"}
    horse_df = pd.concat([horse_df, is_down], axis=1)

    horse_df.fillna(value={'is_down': 0}, inplace=True)
    horse_df['is_down'] = horse_df['is_down'].replace('(降)', 1)

    ## 余分な文字を削除
    horse_df['rank'] = horse_df['rank'].apply(lambda x: x.replace("(降)", ""))
    horse_df['rank'] = horse_df['rank'].apply(lambda x: x.replace("(再)", ""))
    horse_df = horse_df[(horse_df['rank'] != "取") & (horse_df['rank'] != "除") & (horse_df['rank'] != "失")]
    horse_df['rank'] = pd.DataFrame(horse_df['rank'].mask(horse_df['rank'] == "中", 20))
    horse_df['rank'] = horse_df['rank'].astype(int)
    return horse_df

#frame_number

#horse_number

#horse_id

#sex_and_age
def sex_and_age(horse_df):
    #数字のみ抜き出し
    horse_df["age"] = horse_df["sex_and_age"].str.extract('([0-9]+)', expand=True)
    horse_df["age"] = horse_df["age"] .astype(int)
    #それぞれのステータスを数字に置換
    horse_df["sex_and_age"]  = horse_df["sex_and_age"].replace('.*(牡).*', 0,regex=True)
    horse_df["sex_and_age"]  = horse_df["sex_and_age"].replace('.*(牝).*', 1,regex=True)
    horse_df["sex_and_age"]  = horse_df["sex_and_age"].replace('.*(セ).*', 2,regex=True)
    #sexを作成
    horse_df["sex"] = horse_df["sex_and_age"]
    return horse_df

#burden_weight

#rider_id

#goal_time
def goal_time(horse_df):
    horse_df['goal_time'] = pd.to_datetime(horse_df['goal_time'], format='%M:%S.%f') - pd.to_datetime('00:00.0', format='%M:%S.%f')
    horse_df['goal_time'] = horse_df['goal_time'].dt.total_seconds()
    # 欠損値を最大値で埋める
    horse_df.fillna(value={'goal_time': horse_df['goal_time'].max()}, inplace=True)
    return horse_df

#last_time
def last_time(horse_df):
    # 欠損値を最大値で埋める
    horse_df.fillna(value={'last_time': horse_df['last_time'].max()}, inplace=True)
    horse_df["last_time"] = pd.to_numeric(horse_df["last_time"], errors="coerce")
    horse_df["last_time"] = horse_df["last_time"].apply(lambda x: int((x // 100) * 60 + (x % 100) + 0.5))
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
    horse_df["half_way_rank"] = horse_df["half_way_rank"].apply(lambda x: mean([float(n) for n in (x.split("-"))]) if type(x) is str else float(x) )
    horse_df[horse_df["rank"] == 20] = horse_df[horse_df["rank"] == 20].fillna({'half_way_rank': 20})
    horse_df["half_way_rank"] = horse_df["half_way_rank"].fillna(horse_df['half_way_rank'].mean())
    horse_df["half_way_rank"] = horse_df["half_way_rank"].astype(float)
    return horse_df

#horse_weight
def horse_weight(horse_df):
    horse_weight_dif = horse_df["horse_weight"].str.extract('\(([-|+]?\d*)\)', expand=True)
    horse_weight_dif.columns ={"horse_weight_dif"}
    horse_df = pd.concat([horse_df, horse_weight_dif], axis=1)
    horse_df['horse_weight'] = horse_df['horse_weight'].replace('\(([-|+]?\d*)\)', '', regex=True)
    horse_df['horse_weight'] = horse_df['horse_weight'].replace('計不', np.nan)
    horse_df['horse_weight'] = horse_df['horse_weight'].astype(int)
    horse_df['horse_weight_dif'] = horse_df['horse_weight_dif'].astype(int)
    # 計不 の horse_idを探し、馬ごとの平均値で穴埋め
    no_records = horse_df[horse_df['horse_weight'].isnull()]['horse_id']
    for no_record_id in no_records:
        horse_df.loc[(horse_df['horse_id'] == no_record_id)&(horse_df['horse_weight'].isnull()), 'horse_weight'] = horse_df[horse_df['horse_id'] == no_record_id]['horse_weight'].mean() 
        horse_df.loc[(horse_df['horse_id'] == no_record_id)&(horse_df['horse_weight_dif'].isnull()), 'horse_weight_dif'] = 0 
    return horse_df

#goal_time_dif
def goal_time_dif(horse_df):
    horse_df['goal_time_dif'] = horse_df.groupby('race_id')['goal_time'].diff().fillna(0).reset_index(drop=True)
    return horse_df

#burden_weight_rate
def burden_weight_rate(horse_df):
    horse_df['burden_weight_rate'] = horse_df['burden_weight']/horse_df['horse_weight']
    return horse_df

#avg_velocity
def avg_velocity(horse_df,race_df):
    # レース距離情報をmerge
    race_tmp_df = race_df[["race_id", "distance"]]
    horse_df = pd.merge(horse_df, race_tmp_df, on='race_id')
    horse_df["distance"] = horse_df["distance"].astype(int)
    horse_df["avg_velocity"] = horse_df["distance"]/horse_df["goal_time"]
    #オリジナルの削除
    horse_df.drop(['distance'], axis=1, inplace=True)
    return horse_df


##########horse_info_df##########
#horse_id

#bday

#tame_id

#owner_id

#producer_id

#production area
def production_area(horse_info_df):
    horse_info_df['production_area'] = horse_info_df['production_area'].apply(lambda x: x.replace('\n', ''))
    return horse_info_df

#auction price
def auction_price(horse_info_df):
    horse_info_df['auction_price'] = horse_info_df['auction_price'].apply(lambda x: x.replace('\n', ''))
    return horse_info_df

#winnings
def winnings(horse_info_df):
    horse_info_df['winnings'] = horse_info_df['winnings'].apply(lambda x: x.replace('\n', ''))
    return horse_info_df

#lifetime record
def lifetime_record(horse_info_df):
    horse_info_df['lifetime_record'] = horse_info_df['lifetime_record'].apply(lambda x: x.replace('\n', ''))
    return horse_info_df

#wined race title

#inbreeding-1

#inbreeding-2

#father

#faths father

#faths mother

#mother

#moths father

#moths mother

##########horse_race_df##########
#date

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

#distance

#groud_status

#goal_time

#goal_time_dif

#half_way_rank

#pace,last_time

#horse_weight
def horse_weight(horse_race_df):
    horse_weight_dif = horse_race_df["horse_weight"].str.extract('\(([-|+]?\d*)\)', expand=True)
    horse_weight_dif.columns ={"horse_weight_dif"}
    horse_race_df = pd.concat([horse_race_df, horse_weight_dif], axis=1)
    horse_race_df['horse_weight'] = horse_race_df['horse_weight'].replace('\(([-|+]?\d*)\)', '', regex=True)
    horse_race_df['horse_weight'] = horse_race_df['horse_weight'].replace('計不', np.nan)
    horse_race_df['horse_weight'] = horse_race_df['horse_weight'].astype(float)
    horse_race_df['horse_weight_dif'] = horse_race_df['horse_weight_dif'].astype(float)
    # 計不 の horse_idを探し、馬ごとの平均値で穴埋め
    no_records = horse_race_df[horse_race_df['horse_weight'].isnull()]['horse_id']
    for no_record_id in no_records:
        horse_race_df.loc[(horse_race_df['horse_id'] == no_record_id)&(horse_race_df['horse_weight'].isnull()), 'horse_weight'] = horse_race_df[horse_race_df['horse_id'] == no_record_id]['horse_weight'].mean() 
        horse_race_df.loc[(horse_race_df['horse_id'] == no_record_id)&(horse_race_df['horse_weight_dif'].isnull()), 'horse_weight_dif'] = 0 
    return horse_race_df

#runner-up-horse-id

#prize

#horse_id
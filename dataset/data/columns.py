'''スクレイピングするカラムの設定'''

def race_data_columns():
    race_data_columns=[
        'race_id',
        'race_round',
        'race_title',
        'race_course',
        'weather',
        'ground_status',
        'time',
        'date',
        'where_racecourse',
        'total_horse_number',
        'frame_number_first',
        'horse_number_first',
        'frame_number_second',
        'horse_number_second',
        'frame_number_third',
        'horse_number_third',
        'tansyo',
        'hukusyo_first',
        'hukusyo_second',
        'hukusyo_third',
        'wakuren',
        'umaren',
        'wide_1_2',
        'wide_1_3',
        'wide_2_3',
        'umatan',
        'renhuku3',
        'rentan3'
        ]
    return race_data_columns

def horse_data_columns():
    horse_data_columns=[
        'race_id',
        'rank',
        'frame_number',
        'horse_number',
        'horse_id',
        'sex_and_age',
        'burden_weight',
        'rider_id',
        'goal_time',
        'goal_time_dif',
        'time_value',
        'half_way_rank',
        'last_time',
        'odds',
        'popular',
        'horse_weight',
        'tame_time',
        'tamer_id',
        'owner_id'
    ]
    return horse_data_columns


def targethorse_data_columns():
    horse_data_columns=[
        'race_id',
        'frame_number',
        'horse_number',
        'horse_id',
        'sex_and_age',
        'burden_weight',
        'rider_id',
        'tamer_id',
        # 'owner_id',
        'horse_weight',
        'odds',
        'popular',
        'horse_name',
        ]
    return horse_data_columns


def targetrace_data_columns():
    race_data_columns=[
        'race_id',
        'race_title',
        'date',
        'race_round',
        'time',
        'race_course',
        'weather',
        'ground_status',
        'where_racecourse',
        'total_horse_number',
        ]
    return race_data_columns

def horse_info_columns():
    horse_data_info_columns=[
        'horse_id',
        'bday',
        'tamer_id',
        'owner_id',
        'producer_id',
        'production_area',
        'auction_price',
        'winnings',
        'lifetime_record',
        'wined_race_title',
        'inbreeding_1',
        'inbreeding_2',
        'father',
        'faths_father',
        'faths_mother',
        'mother',
        'moths_father',
        'moths_mother'
    ]
    return horse_data_info_columns

def horse_race_columns():
    horse_race_columns=["date",
                        "where_racecourse",
                        "weather",
                        "race_round",
                        "race_title",
                        "race_id",
                        "total_horse_number",
                        "frame_number",
                        "horse_number",
                        "odds",
                        "popular",
                        "rank",
                        "rider_id",
                        "burden_weight",
                        'race_course',
                        #"distance",上のと入れ替え
                        "ground_status",
                        'goal_time',
                        'goal_time_dif',
                        'half_way_rank',
                        'pace',
                        'last_time',
                        'horse_weight',
                        'wined_horse_id',
                        'prize'
                        ]
    return horse_race_columns
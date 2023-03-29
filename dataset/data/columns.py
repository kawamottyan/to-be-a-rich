#スクレイピングするカラムの設定
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
        'owner_id'
        'horse_weight',
        'odds',
        'popular',
        'horse_name',
        ]
    return horse_data_columns


def targetrace_data_columns():
    race_data_columns=[
        'race_id',
        'race_round',
        'race_title',
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
        'tame_id',
        'owner_id',
        'producer_id',
        'production area',
        'auction price',
        'winnings',
        'lifetime record',
        'wined race title',
        'inbreeding-1',
        'inbreeding-2',
        'father',
        'faths father',
        'faths mother',
        'mother',
        'moths father',
        'moths mother'
    ]
    return horse_data_info_columns

def horse_race_columns():
    horse_race_columns=["date",
                        "whereracecourse",
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
                        "horse_wight",
                        "distance",
                        "groud_status",
                        'goal_time',
                        'goal_time_dif',
                        'half_way_rank',
                        'pace',
                        'last_time',
                        'horse_weight',
                        'runner-up-horse-id',
                        'prize'
                        ]
    return horse_race_columns
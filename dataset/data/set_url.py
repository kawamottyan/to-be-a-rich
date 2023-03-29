'''URLを設定する'''

def horse_target():
    URL = "https://race.netkeiba.com/race/shutuba.html?race_id=202307020611&rf=race_list"#race_listのページを指定
    return URL

def race_database():
    URL = "https://db.netkeiba.com/?pid=race_search_detail"
    return URL

def horse_database():
    URL = "https://db.netkeiba.com/?pid=horse_search_detail"
    return URL

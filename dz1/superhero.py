import requests
from pprint import pprint as pprint 

###############################################################################
###############################################################################

BASE_URL   = "https://akabab.github.io/superhero-api/api/"
ALL_DATA   = "all.json"
HERO_DATA  = "id/"          # id/1.json
HERO_STATS = "powerstats/"  # powerstats/1.json

###############################################################################
###############################################################################

# Запрос данных о всех героях по HTTP
# RETURN
#   список героев (распаршенный JSON)
def request_all_data():
    res = requests.request('GET', BASE_URL + ALL_DATA)
    # проверка на ошибку
    if res.ok:
        return res.json()
    return []

# Определение ID героя по имени
# PARAMS
#   DATA - список всех героев
#   NAME - искомое имя героя
# RETURN
#   ID героя ИЛИ FALSE (если герой не найден)
def get_hero_id(data, name):
    for hero in data:
        if hero['name'] == name:
            return hero['id']
    return False 

# Запрос статов героя по его ID
# PARAMS
#   HERO_ID - ID героя
# RETURN
#   словарь со статами {'stat1': value1, 'stat2: value2, ...}
#   ИЛИ
#   FALSE (если ошибка)
def request_hero_powerstats(hero_id):
    res = requests.request('GET', BASE_URL + HERO_STATS + f'{hero_id}.json')
    # проверка на ошибку
    if res.ok:
        return res.json()
    return False

# Запрос статов героев по имени
# PARAMS
#   HERO_NAMES - список имен героев (['name1', 'name2', ...])
#   DATA - массив данных всех героев (необязательный)
# RETURN
#   список с параметрами героев в формате: [
#       { 'id', 'name', 'powerstats'},
#       ...
# ]
def request_heroes_powerstats(hero_names, data = []):
    # если данных по героям нет - запросим их
    if len(data) == 0:
        data = request_all_data()
    
    heroes_data = []
    # цикл по всем именам героев из параметра функции
    for hero in hero_names:
        # определение ID героя
        hero_id = get_hero_id(data, hero)
        # получение статов героя
        hero_stats = request_hero_powerstats(hero_id)
        # проверка на ошибку (что не FALSE)
        if hero_stats:
            heroes_data += [{
                'id': hero_id,
                'name': hero,
                'powerstats': hero_stats
                }]
    # возвращаем итоговый список
    return heroes_data

# Поиск лучшего героя по указанному стату
# PARAMS
#   HERO_NAMES - список имен героев (['name1', 'name2', ...])
#   POWERSTAT - стат героя ('intelligence', 'strength', 'speed', 'durability', 'power', 'combat')
#   DATA - массив данных всех героев (необязательный)
# RETURN
#   словарь с данными по лучшему герою в формате: { 'id', 'name', 'powerstats'}
def find_best_of(hero_names, powerstat, data = []):
    # получение статов героев из hero_names
    heroes_data = request_heroes_powerstats(hero_names, data)
    best_hero = {}
    # в цикле по героям ищем того, кто имеет наибольшее значение powerstat
    for hero in heroes_data:
        if hero['powerstats'].get(powerstat, 0) > best_hero.get('powerstats',{}).get(powerstat, 0):
            best_hero = hero
    return best_hero

###############################################################################
###############################################################################

def __main__():
    #res = requests.request('GET', BASE_URL + ALL_DATA)
    #data = res.json()
    #pprint(data)
   
    heroes = ['Hulk', 'Captain America', 'Thanos', '111', 'Batman']
    stat = 'intelligence'   # 'intelligence', 'strength', 'speed', 'durability', 'power', 'combat'
 
    res = request_heroes_powerstats(heroes)
    pprint(res)
 
    best = find_best_of(heroes, stat)
    print(f'Best in {stat} is {best["name"]}')
    pprint(best)


###############################################################################
###############################################################################

__main__()

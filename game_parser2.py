
import os
import json
import tomllib
import sqlite3
import requests
import wget


with open("config.toml", "rb") as f:
        config = tomllib.load(f)


def search_game_inDB(query_title):
    con = sqlite3.connect("games.db")
    cur = con.cursor()

    query = """
        select title
        from game 
        where lower(title) like lower(?) 
        LIMIT 10;
    """  

    res = cur.execute(query, [query_title + '%'])

    payload = res.fetchall()
    
    game_results = [ element[0] for element in payload]

    return game_results

def search_game_title(title):

    if os.path.isdir(os.path.join(config['CACHE_DIR'], title)):

        game_dir = os.path.join(config['CACHE_DIR'], title)

        print(f"Found cached information in {game_dir}")

        with open(os.path.join(game_dir, 'game_data.json')) as json_file:
            game_data = json.load(json_file)

            return game_data, os.path.join(game_dir, 'image.jpg')
    else:
        print('Game not in cache')
        return None

def search_game_with_API(title):
    payload = {'api_key': config['APIKEY'], 
        'format': 'json',
        'resources': 'game',
        'limit': 10,
        'field_list': 'name,guid',
        'query': title}
    
    response = requests.get('https://www.giantbomb.com/api/search/',
                     params=payload,
                     headers = {"User-Agent": "guicli-call"})
    
    response.raise_for_status()
    
    raw_data = response.json()

    return raw_data['results']


def fetch_game_guid(title):
     # first perform a search with the game's title to find it's guid

        
    payload = {'api_key': config['APIKEY'], 
            'format': 'json',
            'resources': 'game',
            'limit': 1,
            'field_list': 'guid',
            'query': title}
    
    response = requests.get('https://www.giantbomb.com/api/search/',
                     params=payload,
                     headers = {"User-Agent": "guicli-call"})
    
    response.raise_for_status()
    
    raw_data = response.json()

    #print(raw_data)

    '''
    {
        'error': 'OK',
        'limit': 1,
        'offset': 0, 
        'number_of_page_results': 1, 
        'number_of_total_results': 362, 
        'status_code': 1, 
        'results': [
            {'guid': '3030-2512', 
            'resource_type': 'game'}
            ], 
        'version': '1.0'}

    '''

    game_guid = raw_data['results'][0]['guid']

    return game_guid


def fetch_game_data(guid):

    # check if game is cached

    if os.path.isdir(os.path.join(config['CACHE_DIR'], guid)):

        game_dir = os.path.join(config['CACHE_DIR'], guid)
        print(f"Found cached information in {game_dir}")
        return
     
    # use the guid to fetch the necessary game info

    payload = {'api_key': config['APIKEY'], 
            'format': 'json',
            'field_list': 'image,genres,platforms,developers,publishers,name,original_release_date'}
    
    response = requests.get(f'https://www.giantbomb.com/api/game/{guid}/',
                     params=payload,
                     headers = {"User-Agent": "guicli-call"})
    
    response.raise_for_status()
    
    raw_data = response.json()

    game_data = {'title': raw_data['results']['name'],
                'original_release_date':raw_data['results']['original_release_date'],
                'platforms': raw_data['results']['platforms'],
                'developers': raw_data['results']['developers'],
                'publishers': raw_data['results']['publishers'],
                'genres': raw_data['results']['genres'],
                'guid': guid}

    entries_to_remove = ('api_detail_url', 'id', 'site_detail_url', 'abbreviation')

    for element in game_data['platforms']:
        for e in entries_to_remove:
            element.pop(e, None)

    for element in game_data['developers']:
        for e in entries_to_remove:
            element.pop(e, None)

    for element in game_data['publishers']:
        for e in entries_to_remove:
            element.pop(e, None)

    for element in game_data['genres']:
        for e in entries_to_remove:
            element.pop(e, None)

    #print(game_data)
            
    os.mkdir(os.path.join(config['CACHE_DIR'], guid))

    with open(os.path.join(config['CACHE_DIR'], guid, 'game_data.json'), 'w') as f:
        json.dump(game_data, f, indent=4)


    image_url = str(raw_data['results']['image']['original_url'])
    image_url = image_url.replace('\\','')

    #print(image_url)

    wget.download(image_url, os.path.join(config['CACHE_DIR'],guid,'image.jpg'), bar=False)
    

def search_cache_data(guid):
    if os.path.isdir(os.path.join(config['CACHE_DIR'], guid)):

        game_dir = os.path.join(config['CACHE_DIR'], guid)

        print(f"Found cached information in {game_dir}")

        with open(os.path.join(game_dir, 'game_data.json')) as json_file:
            game_data = json.load(json_file)

            return game_data, os.path.join(game_dir, 'image.jpg')
    else:
        print('Game not in cache!')
        return None
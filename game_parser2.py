
import os
import json
import tomllib
import sqlite3

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
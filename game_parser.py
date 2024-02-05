import click
import sqlite3
import requests
import os
import wget
import json
import tomllib

with open("config.toml", "rb") as f:
        config = tomllib.load(f)

@click.command()

@click.option('--title', prompt='Type your game\'s title',
              help='The game title that will be searched in the database')

def cli_search_game_title(title):

    con = sqlite3.connect("games.db")
    cur = con.cursor()

    query = """
        select title
        from game 
        where lower(title) like ? 
        LIMIT 10;
    """  

    res = cur.execute(query, [title + '%'])

    payload = res.fetchall()

    if (payload is None) or (len(payload)==0):
        click.echo(f"No games found...")
        return

    for index, obj in enumerate(payload):
        click.echo(f"{index+1} '{obj[0]}'")

    value = -1

    while (value < 0 or value > len(payload)):
        value = click.prompt(f'Choose game to fetch: [1-{len(payload)}]', type=int)

    if value == 0: return

    target = payload[value-1][0]

    if os.path.isdir(os.path.join(config['CACHE_DIR'], target)):
        click.echo(f"Found cached information")
        return
    else:
        parse_game(target)


def parse_game(database_title):

        click.echo(f"Fetching information for '{database_title}'")

        base_url = 'https://www.giantbomb.com/api/search/'

        url_options = '&format=json&resources=game&limit=1'

        full_url = base_url + '?api_key=' + config['APIKEY'] + url_options + '&query="' + database_title +'"'
                     

        # A GET request to the API
        response = requests.get(full_url, 
                                headers = {"User-Agent": "guicli-call"})
        response.raise_for_status()
        
        raw_data = response.json()

        #print(raw_data)

        game_data = {'title': database_title,
                     'original_release_date':raw_data['results'][0]['original_release_date'],
                     'platforms': raw_data['results'][0]['platforms']}

        entries_to_remove = ('api_detail_url', 'id', 'site_detail_url', 'abbreviation')

        for element in game_data['platforms']:
            for e in entries_to_remove:
                element.pop(e, None)


        os.mkdir(os.path.join(config['CACHE_DIR'],database_title))

        with open(os.path.join(config['CACHE_DIR'],database_title,'game_data.json'), 'w') as f:
            json.dump(game_data, f, indent=4)


        
        image_url = str(raw_data['results'][0]['image']['original_url'])
        image_url = image_url.replace('\\','')

        #print(image_url)


        wget.download(image_url, os.path.join(config['CACHE_DIR'],database_title,'image.jpg'), bar=False)
        

if __name__ == '__main__':
    cli_search_game_title()
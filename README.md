# Python Game Tiermaker
A cross-platform desktop GUI app that lets you create a tierlist of video games. The app uses the API provided by [giantbomb.com](giantbomb.com) to search for and download game cover images.

# Overview

![Peek 2024-02-09 03-49](https://github.com/mataktelis11/python-game-parser/assets/61196956/d67c108f-bf05-4c08-a3a0-6a75fd8a69e7)

# Requirements
- Python 3 (vresion 3.11 was used)
- git

For Unix:
```bash
$ git clone https://github.com/mataktelis11/python-game-parser.git
$ python3 -m venv guienv
$ source guienv/bin/activate
$ pip install -r requirements.txt
```

For Windows:
```cmd
$ git clone https://github.com/mataktelis11/python-game-parser.git
$ python -m venv guienv
$ guienv\Scripts\activate.bat
$ pip install -r requirements.txt
```

Since this app is **purely experimental**, the API key is **not** provided. You can create your own key by registering an account in [giantbomb.com](giantbomb.com).

To run the app you also need to create a ```config.tom``` file that looks like this:
```toml
APIKEY = 'YOUR API KEY'
CACHE_DIR = 'YOUR CACHE FOLDER'
tiers = ['S', 'A', 'B', 'C', 'D']
tiersColors = ['#c42708', '#c47608', '#bec408', '#79c408', '#08c486']
```
You also need to create an empty folder and specify it as the ```CACHE_DIR``` in ```config.tom```.

# Notes 
- The app was mostly tested on Debian 12 Linux. If you find bugs in your own OS, you can raise an issue.
- The app doesn't use drag n drop for the creation of the tierlists.
- Any sources used are directly referenced in the code as links.
- If you have any comments or suggestions, feel free to do a pull request.


# In-development screenshots:
![Screenshot from 2024-02-08 03-12-57](https://github.com/mataktelis11/python-game-parser/assets/61196956/0355de4d-f960-46e1-bd42-da2095fa199a)

![Screenshot from 2024-02-09 01-03-26](https://github.com/mataktelis11/python-game-parser/assets/61196956/4c5b409d-ad72-46d9-92e7-6a6306ce15c1)

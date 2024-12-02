from datetime import datetime
from pathlib import Path

import constants as c
from google_docs.doc_creator import DocCreator
from database import database
from html_reports import generator

if __name__ == '__main__':
    db = database.Database()
    all_games = db.get_all(c.get_games)
    game_output, game_info = c.write_games(all_games)
    game = game_info[input(game_output)]
    choice = input('Enter 1 for Pre Game, 2 for Post Game: ')
    report = c.choices.get(choice, None)[0](db, game[0])
    report.generate()
    players = db.get_all(c.get_player_info.format(game[0][1]))
    requests, file = c.choices.get(choice, None)[1](report, game[1:], players)
    creator = DocCreator()
    print(creator.create_doc(file, requests))




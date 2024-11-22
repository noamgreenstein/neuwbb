from datetime import datetime
from pathlib import Path

import constants as c
import sqlite3
from database import database
from html_reports import generator

if __name__ == '__main__':
    db = database.Database()
    all_games = db.get_all(c.get_games)
    game_output, game_info = c.write_games(all_games)
    game = game_info[input(game_output)]
    choice = input('Enter 1 for Pre Game, 2 for Post Game: ')
    report = c.choices.get(choice, None)(db, game[0])
    report.generate()
    players = db.get_all(c.get_player_info.format(game[0][1]))
    html = generator.pregame(report, game[1:], players)
    file = open('/Users/noamgreenstein/Documents/Projects/NEUWBB24/reports/newrep.html', 'w')
    file.write(html)
    file.close()
    print('Report Generated')



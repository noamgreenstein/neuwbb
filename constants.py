import datetime

from reporting.pregame import PreGameReport

choices = {
    '1': PreGameReport
}

get_games = '''
select g.game_id, g.game_date, g.home_id, g.away_id, t1.name, t2.name, t1.abbrev, t2.abbrev
from neu_schedule n
join games g on n.game_id = g.game_id 
join teams t1 on t1.team_id = g.home_id
join teams t2 on t2.team_id = g.away_id
'''

get_player_info = '''
select name_first || " " || name_last ,
        jersey_num,
        case when player_pos = "F" then "Forward"
            when player_pos = "C" then "Center"
            else "Guard" end,
        case when year = "FR" then "Freshman"
            when year = "SO" then "Sophomore"
            when year = "JR" then "Junior"
            else "Senior" end,
        height_feet || "-" || height_inches
from players
where team_id = {}
'''

def write_games(all_games):
    output = 'Select A Game:\n\n'
    output_info = {}
    for i, game in enumerate(all_games):
        away = game[3]
        home = game[2]
        game_details = ('@', game[4]) if away == 1 else ('Vs.', game[5])
        game_str = f'{i + 1}. {game_details[0]} {game_details[1]}\n'
        output += game_str
        output_info[str(i + 1)] = ((game[0], home if away == 1 else away),
                                   game_str,
                                   game[1],
                                   game[6] if away == 1 else game[7])
    output += 'Enter Game #: '
    return output, output_info

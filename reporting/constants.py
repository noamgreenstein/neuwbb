get_game = """select game_id
from neu_schedule
where played = False
order by game_id
limit 1"""

get_teams = '''
select home_id, away_id
from games
where game_id = {}
limit 1
'''

get_link = '''
select bball_ref
from teams 
where team_id = {}
limit 1
'''

get_players = '''
select name_first || ' ' || name_last
from players
where team_id = {}
'''

get_players_id = '''
select name_first || ' ' || name_last as player_name, player_id, jersey_num, bball_ref
from players
where team_id = {}
'''

get_player_by_name = '''
select player_id
from players
where team_id = {}
and name_first = \"{}\" 
and name_last = \"{}\" 
'''

get_player_links = '''
select name_first || ' ' || name_last, bball_ref
from players
where team_id = {}
'''

insert_mark = '''
    insert into benchmarks (game_id, target_id, over, value, stat)  values {}
'''

get_marks = '''
select * from benchmarks where game_id = {}
'''

mark_value = "({},{},{},{},'{}'),"

get_ref_name = 'select ref_name from teams where team_id = {}'

neu_link = 'https://www.sports-reference.com/cbb/schools/northeastern/women/2025.html'


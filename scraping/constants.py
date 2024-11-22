unnamed_level = 'Unnamed: {}_level_{}'

rename_cols = {
    'Tm': 'School/pts',
    'Opp_2': 'Opponent/pts'
}

drop_cols = [
    unnamed_level.format('2', '1'),
    unnamed_level.format('23', '1'),
    'Opp_1',
    'G',
    'Date'
]

num_cols = ['School/pts', 'Opponent/pts', 'School/FG', 'School/FGA', 'School/FG%', 'School/3P',
            'School/3PA', 'School/3P%', 'School/FT', 'School/FTA', 'School/FT%', 'School/ORB',
            'School/TRB', 'School/STL', 'School/BLK', 'School/TOV', 'School/PF', 'Opponent/FG',
            'Opponent/FGA', 'Opponent/FG%', 'Opponent/3P', 'Opponent/3PA', 'Opponent/3P%',
            'Opponent/FT', 'Opponent/FTA', 'Opponent/FT%', 'Opponent/ORB', 'Opponent/TRB',
            'Opponent/STL', 'Opponent/BLK', 'Opponent/TOV', 'Opponent/PF']

game_logs = '-gamelogs.html'

player_logs = '/gamelog/2024'

drop_player_cols = ['Rk', 'Date', 'School', 'Unnamed: 3', 'Opponent', 'Type', 'GS', 'GmSc']

def cols_to_str(cols):
    result = []
    for col in cols:
        result.append((col[0] + '/' + col[1]) if 'Unnamed' not in col[0] else col[1])
    return result

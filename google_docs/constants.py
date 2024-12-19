replace_text = {
    'replaceAllText': {
        'containsText': {
            'text': '',
            'matchCase': True
        },
        'replaceText': ''}}

team_colors = {
    2: ('550000', 'black'),
    3: ('FFFFFF', 'black'),
    4: ('90EE91', 'black'),
    5: ('B22222', 'black'),
    6: ('008631', 'black'),
    7: ('ADD8E6', 'black'),
    8: ('572932', 'black'),
    9: ('b042ff', 'black'),
    10: ('602D89', 'black'),
    11: ('0A2240', 'white'),
    12: ('FFC600', 'black'),
    13: ('006666', 'black'),
    14: ('FFBB00', 'black'),
    16: ('115740', 'white'),
    17: ('1f355e', 'black'),
    18: ('EA7125', 'black'),
    19: ('00539f', 'white'),
    20: ('A79E70', 'black'),
    21: ('004684', 'white'),
    22: ('6d9eeb', 'black'),
    23: ('19305E', 'white'),
    24: ('B59A57', 'black')
}

tables = [7, 9]

summary_stats = {
    'PPG': 'ppg_text',
    'RPG': 'rpg_text',
    'APG': 'apg_text',
    'FG%': 'fgpct_text',
    '3P%': '3ppct_text',
    'FT%': 'ftpct_text'
}

benchmarks = {
    'School/pts': 'obm1',
    'Opponent/pts': 'nbm1',
    'School/FGA': 'obm2',
    'Opponent/FGA': 'nbm2',
    'School/FG': 'obm3',
    'Opponent/FG': 'nbm3',
    'School/FG%': 'obm4',
    'Opponent/FG%': 'nbm4',
    'School/3PA': 'obm5',
    'Opponent/3PA': 'nbm5',
    'School/3P': 'obm6',
    'Opponent/3P': 'nbm6',
    'School/3P%': 'obm7',
    'Opponent/3P%': 'nbm7',
    'School/AST': 'obm8',
    'Opponent/AST': 'nbm8',
    'School/ATO': 'obm9',
    'Opponent/ATO': 'nbm9',
    'School/FTA': 'ob1',
    'Opponent/FTA': 'nb1',
    'School/FT': 'ob2',
    'Opponent/FT': 'nb2',
    'School/FT%': 'ob3',
    'Opponent/FT%': 'nb3',
    'School/ORB': 'ob4',
    'Opponent/ORB': 'nb4',
    'School/DRB': 'ob5',
    'Opponent/DRB': 'nb5',
    'School/BLK': 'ob6',
    'Opponent/BLK': 'nb6',
    'School/STL': 'ob7',
    'Opponent/STL': 'nb7',
    'School/TOV': 'ob8',
    'Opponent/TOV': 'nb8',
    'School/PF': 'ob9',
    'Opponent/PF': 'nb9'
}

dash = '     -'

team_percentiles = [f'pctl{i}' for i in range(1, 10)] + ['pctl_1']
opp_percentiles = [f'{i}pctl' for i in range(1, 10)] + ['1_pctl']

ws_table = 838

win_share_info = ['name', '#', 'pos', 'grade', 'height', 'ws']

box_scores = {
    'Opponent/pts': 'neu_pts',
    'Opponent/AST': 'neu_ast',
    'Opponent/ORB': 'neu_orb',
    'Opponent/DRB': 'neu_drb',
    'Opponent/BLK': 'neu_blk',
    'Opponent/STL': 'neu_stl',
    'Opponent/TOV': 'neu_tov',
    'School/pts': 'opp_pts',
    'School/AST': 'opp_ast',
    'School/ORB': 'opp_orb',
    'School/DRB': 'opp_drb',
    'School/BLK': 'opp_blk',
    'School/STL': 'opp_stl',
    'School/TOV': 'opp_tov',
}

averages = {
    'School/pts': ('_pts', 1),
    'School/AST': ('_ast', 2),
    'School/ORB': ('_orb', 3),
    'School/DRB': ('_drb', 4),
    'School/BLK': ('_blk', 6),
    'School/STL': ('_stl', 5),
    'School/TOV': ('_tov', 7),
}

diffs = {
    (False, True): 'FFFFFF',
    (True, False): '93c47d',
    (False, False): 'ea9999'
}
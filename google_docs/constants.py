import copy

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


def insert_mark_request(text):
    return {
        'insertText': {
            'text': text,
            'location': {
                'segmentId': '',
                'index': 1081
            }
        }
    }


def format_replace(text):
    tmp = copy.deepcopy(replace_text)
    tmp['replaceAllText']['containsText']['text'] = text
    return tmp


def get_marks(mark, name):
    if mark['AUC'] >= .7:
        opt_val = mark['optimal amount']
        drt = mark['direction']
        pct = '%' in name
        if str(opt_val) != 'nan' and drt != 'Flat':
            ou = "O" if drt == "Reverse" else "U"
            val = f'{int(round(opt_val * 100, 0)) if pct else int(round(opt_val, 0))}'
            return ou + val + '%' if pct else ou + val
    return dash


def hex_to_rgb(hex_color):
    # Remove the '#' if present
    hex_color = hex_color.lstrip('#')
    # Convert hex to RGB values (0-255)
    rgb = tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
    # Convert to 0-1 range
    return {
        'red': rgb[0] / 255,
        'green': rgb[1] / 255,
        'blue': rgb[2] / 255
    }


def format_bg_change(index, row, column, color):
    return format_cell_request(
        table_cell_location={
            'tableStartLocation': {'index': index, 'segmentId': ''},
            'rowIndex': row,
            'columnIndex': column
        },
        background_hex=color
    )


def format_cell_request(table_cell_location, background_hex=None):
    fields = []
    table_cell_style = {}

    # Set background color if provided
    if background_hex:
        rgb_color = hex_to_rgb(background_hex)
        table_cell_style['backgroundColor'] = {
            'color': {
                'rgbColor': rgb_color
            }
        }
        fields.append('backgroundColor')

    # Construct the complete request
    format_request = {
        'updateTableCellStyle': {
            'tableCellStyle': table_cell_style,
            'fields': ','.join(fields),
            'tableRange': {
                'tableCellLocation': table_cell_location,
                "rowSpan": 1,
                "columnSpan": 1
            }
        }
    }

    return format_request


def format_request(old_text, new_text):
    req = format_replace(old_text)
    req['replaceAllText']['replaceText'] = new_text
    return req


def order_percentiles(data):
    percentiles = [[] for _ in range(10)]
    for pctl in data:
        pct = pctl[1] if pctl[0] not in ['PF', 'TOV'] else 100 - pctl[1]
        amt = pctl[2] if '%' not in pctl[0] else round(100 * float(pctl[2]), 1)
        if pct <= 1:
            percentiles[9].append(f'{pctl[0]}({amt})')
        if pct <= 2:
            percentiles[8].append(f'{pctl[0]}({amt})')
        if pct <= 5:
            percentiles[7].append(f'{pctl[0]}({amt})')
        if pct <= 10:
            percentiles[6].append(f'{pctl[0]}({amt})')
        if pct <= 20:
            percentiles[5].append(f'{pctl[0]}({amt})')
        if pct >= 80:
            percentiles[4].append(f'{pctl[0]}({amt})')
        if pct >= 90:
            percentiles[3].append(f'{pctl[0]}({amt})')
        if pct >= 95:
            percentiles[2].append(f'{pctl[0]}({amt})')
        if pct >= 98:
            percentiles[1].append(f'{pctl[0]}({amt})')
        if pct >= 99:
            percentiles[0].append(f'{pctl[0]}({amt})')
    return percentiles


def percentile_requests(request_text, percentiles):
    requests = []
    for i, text in enumerate(request_text):
        if len(percentiles[i]) > 0:
            requests.append(format_request(text, '\n'.join(percentiles[i])))
        else:
            requests.append(format_request(text, ''))
    return requests


def player_marks(player, data):
    text = f'\n{player}\nWant her:\n'
    mark_text = ''
    for mark in data:
        if data[mark]['AUC'] >= .7:
            opt_val = data[mark]['optimal amount']
            drt = data[mark]['direction']
            pct = '%' in mark
            if str(opt_val) != 'nan' and drt != 'Flat':
                ou = "OVER" if drt == "Reverse" else "UNDER"
                mark_text += f'- {ou} {round(opt_val * 100, 0) if pct else int(round(opt_val, 0))} {mark}\n'

    return text + mark_text if len(mark_text) > 0 else ''


def update_color(start, end, is_white):
    color = 1 if is_white else 0
    return {
        'updateTextStyle': {
            'textStyle': {
                'foregroundColor': {
                    'color': {
                        'rgbColor': {
                            "red": color,
                            "green": color,
                            "blue": color
                        }
                    }
                }
            },
            'fields': 'foregroundColor',
            'range': {
                "segmentId": '',
                "startIndex": start,
                "endIndex": end,
            }
        }
    }

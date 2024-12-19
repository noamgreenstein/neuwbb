from google_docs.constants import replace_text, dash
import copy


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
        pct = 100 - pctl[1] if pctl[0] not in ['PF', 'TOV'] else pctl[1]
        amt = pctl[2] if '%' not in pctl[0] else round(100 * float(pctl[2]), 1)
        if pct <= 1:
            percentiles[9].append(f'{pctl[0]}({amt})')
        elif pct <= 2:
            percentiles[8].append(f'{pctl[0]}({amt})')
        elif pct <= 5:
            percentiles[7].append(f'{pctl[0]}({amt})')
        elif pct <= 10:
            percentiles[6].append(f'{pctl[0]}({amt})')
        elif pct <= 20:
            percentiles[5].append(f'{pctl[0]}({amt})')

        if pct >= 99:
            percentiles[0].append(f'{pctl[0]}({amt})')
        elif pct >= 98:
            percentiles[1].append(f'{pctl[0]}({amt})')
        elif pct >= 95:
            percentiles[2].append(f'{pctl[0]}({amt})')
        elif pct >= 90:
            percentiles[3].append(f'{pctl[0]}({amt})')
        elif pct >= 80:
            percentiles[4].append(f'{pctl[0]}({amt})')
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


def mark_summary(stats, marks):
    exceeded = []
    failed = []
    stats.index = [str(idx).lower() for idx in stats.index]
    for mark in marks:
        stat = mark[4].lower()
        display_stat = stat.upper().split("/")[1] if '/' in stat else stat.upper()
        val = int(stats.loc[stat]) if '%' not in stat else round(float(stats.loc[stat]) * 100, 1)
        is_over = mark[2] == 1
        mark_str = f'{display_stat} {"OVER" if is_over else "UNDER"} {mark[3]} ({val})'
        if (is_over and mark[3] < val) or (not is_over and mark[3] > val):
            exceeded.append(mark_str)
        else:
            failed.append(mark_str)

    return (f'{len(exceeded)}/{len(marks)}',
            ', '.join(exceeded) if len(exceeded) > 0 else 'None',
            ', '.join(failed) if len(failed) > 0 else 'None')

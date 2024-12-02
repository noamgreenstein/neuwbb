from reporting.pregame import PreGameReport
import google_docs.constants as c


# [124, 301, 512, 682, 838]
def pregame(pregame_data: PreGameReport, game_data, players):
    requests = []
    colors = c.team_colors[pregame_data.opp]

    # change text color
    requests.append(c.update_color(240,244, colors[1] == 'white'))
    requests.append(c.update_color(407,411, colors[1] == 'white'))

    # change bg color
    for table in [124, 301]:
        requests.append(c.format_bg_change(table, 2, 0, colors[0]))
    for i in range(6):
        requests.append(c.format_bg_change(836, 0, i, colors[0]))

    # player benchmarks
    for player in pregame_data.player_data:
        mark_text = c.player_marks(player, pregame_data.player_data[player])
        if mark_text != '':
            requests.append(c.insert_mark_request(mark_text))

    # header
    header_text = f'Northeastern{game_data[0][2:-1]}'
    requests.append(c.format_request('header_text', header_text))
    requests.append(c.format_request('header_date', game_data[1]))

    # Team details
    for stat in pregame_data.summary:
        requests.append(c.format_request(c.summary_stats[stat],
                                         str(pregame_data.summary[stat]) if '%' not in stat else str(round(pregame_data.summary[stat] * 100, 1))))

    # benchmarks
    requests.append(c.format_request('opp_', game_data[2]))
    for mark in c.benchmarks:
        mark_text = c.get_marks(pregame_data.team_data[mark], mark)
        requests.append(c.format_request(c.benchmarks[mark], mark_text))

    # percentiles
    opp_name = game_data[0][2:].strip('Vs. ').strip('@ ').strip('\n')
    requests.append(c.format_request('oppname', opp_name))
    team_percentiles = c.order_percentiles(pregame_data.percentiles['Team'])
    opp_percentiles = c.order_percentiles(pregame_data.percentiles['Team'])
    requests.extend(c.percentile_requests(c.team_percentiles, team_percentiles))
    requests.extend(c.percentile_requests(c.opp_percentiles, opp_percentiles))

    # win share %s
    for i, player in enumerate(list(pregame_data.win_shares[0])):
        for j, data in enumerate(players[i]):
            text = c.win_share_info[j] + str(i + 1)
            if 'height' in text:
                data_str = str(data)[:-2]
            else:
                data_str = str(data)
            requests.append(c.format_request(text, data_str))
        requests.append(c.format_request(f'ws{str(i + 1)}', str(pregame_data.win_shares[0][player])))


    # footer
    footer_text = f'{game_data[1].split(" ")[0]} {game_data[1].split(" ")[2]}'
    footer = c.format_replace('footer_text')
    footer['replaceAllText']['replaceText'] = footer_text
    requests.append(footer)

    return requests, game_data[2] + ' Pregame'


def postgame():
    return []

from reporting.pregame import PreGameReport
from reporting.postgame import PostGameReport
import google_docs.constants as c
import google_docs.functions as f


def pregame(pregame_data: PreGameReport, game_data, players):
    requests = []
    colors = c.team_colors[pregame_data.opp]

    # change text color
    requests.append(f.update_color(240, 244, colors[1] == 'white'))
    requests.append(f.update_color(407, 411, colors[1] == 'white'))

    # change bg color
    for table in [124, 301]:
        requests.append(f.format_bg_change(table, 2, 0, colors[0]))
    for i in range(6):
        requests.append(f.format_bg_change(836, 0, i, colors[0]))

    # player benchmarks
    for player in pregame_data.player_data:
        mark_text = f.player_marks(player, pregame_data.player_data[player])
        if mark_text != '':
            requests.append(f.insert_mark_request(mark_text))

    # header
    header_text = f'Northeastern{game_data[0][2:-1]}'
    requests.append(f.format_request('header_text', header_text))
    requests.append(f.format_request('header_date', game_data[1]))

    # Team details
    for stat in pregame_data.summary:
        requests.append(f.format_request(c.summary_stats[stat],
                                         str(pregame_data.summary[
                                                 stat]) if '%' not in stat else str(
                                             round(pregame_data.summary[stat] * 100, 1))))

    # benchmarks
    requests.append(f.format_request('opp_', game_data[2]))
    for mark in c.benchmarks:
        mark_text = f.get_marks(pregame_data.team_data[mark], mark)
        requests.append(f.format_request(c.benchmarks[mark], mark_text))

    # percentiles
    opp_name = game_data[0][2:].strip('Vs. ').strip('@ ').strip('\n')
    requests.append(f.format_request('oppname', opp_name))
    team_percentiles = f.order_percentiles(pregame_data.percentiles['Team'])
    opp_percentiles = f.order_percentiles(pregame_data.percentiles['Opponent'])
    requests.extend(f.percentile_requests(c.team_percentiles, team_percentiles))
    requests.extend(f.percentile_requests(c.opp_percentiles, opp_percentiles))

    # win share %s
    for i, player in enumerate(list(pregame_data.win_shares[0])):
        for j, data in enumerate(players[i]):
            text = c.win_share_info[j] + str(i + 1)
            if 'height' in text:
                data_str = str(data)[:-2]
            else:
                data_str = str(data)
            requests.append(f.format_request(text, data_str))
        requests.append(
            f.format_request(f'ws{str(i + 1)}', str(pregame_data.win_shares[0][player])))

    # footer
    footer_text = f'{game_data[1].split(" ")[0]} {game_data[1].split(" ")[2]}'
    footer = f.format_replace('footer_text')
    footer['replaceAllText']['replaceText'] = footer_text
    requests.append(footer)
    return requests, game_data[2] + ' Pregame'


def postgame(postgame_data: PostGameReport, game_data, players):
    requests = []
    colors = c.team_colors[postgame_data.opp]
    school_name = ' '.join(game_data[0].split(' ')[2:]).strip('\n')

    # Change Background for table
    for i in range(4):
        requests.append(f.format_bg_change(654, 0, i, colors[0]))

    # Avg Stats
    q = []
    for stat in c.box_scores:
        val = int(postgame_data.box_score[stat])
        is_neu = 'Opponent' in stat
        avg_col = 'School/' + stat.split('/')[1] if is_neu else stat
        info = c.averages[avg_col]
        avg_replace = 'neu_avg' + info[0] if is_neu else 'opp_avg' + info[0]
        avg = round(postgame_data.neu_stats[avg_col].mean(), 1) if is_neu else round(postgame_data.opp_stats[stat].mean(), 1)
        diff = round(val - avg, 1)
        diff_col = 'neu_diff' + info[0] if is_neu else 'opp_diff' + info[0]
        diff_color = c.diffs[(val > avg, val == avg)]
        table_idx = 176 if is_neu else 654

        q.append(f.format_request(c.box_scores[stat], str(val)))
        q.append(f.format_request(avg_replace, str(avg)))
        q.append(f.format_request(diff_col, str(diff)))
        requests.append(f.format_bg_change(table_idx, info[1], 3, diff_color))



    requests.extend(q)
    # Header
    header_text = (f'Northeastern {postgame_data.box_score["Opponent/pts"]} - '
                   f'{postgame_data.box_score["School/pts"]} {school_name}')
    requests.append(f.format_request('header_text', header_text))
    requests.append(f.format_request('header_date', game_data[1]))

    # Benchmark Summary
    neu_marks = [bm for bm in postgame_data.benchmarks if 'Opponent' in bm[4]]
    opp_marks = [bm for bm in postgame_data.benchmarks if 'School' in bm[4]]

    neu_scores = [idx for idx in postgame_data.box_score.index if 'Opponent' in idx]
    opp_scores = [idx for idx in postgame_data.box_score.index if 'School' in idx]

    neu_marks = f.mark_summary(postgame_data.box_score.loc[neu_scores], neu_marks)
    opp_marks = f.mark_summary(postgame_data.box_score.loc[opp_scores], opp_marks)
    requests.append(f.format_request('neu_marks', neu_marks[0]))
    requests.append(f.format_request('neu_exceded', neu_marks[1]))
    requests.append(f.format_request('neu_failed', neu_marks[2]))
    requests.append(f.format_request('opp_marks', opp_marks[0]))
    requests.append(f.format_request('opp_exceeded', opp_marks[1]))
    requests.append(f.format_request('opp_failed', opp_marks[2]))

    # Player Benchmarks
    player_marks_text = ''
    all_player_marks = [bm for bm in postgame_data.benchmarks if '/' not in bm[4]]
    for player in postgame_data.players:
        player_marks = [bm for bm in all_player_marks if bm[1] == player[1]]
        if len(player_marks) > 0:
            player_marks_summary = f.mark_summary(postgame_data.player_stats[player[1]], player_marks)
            player_header = f'{player[0]} #{player[2]}: {player_marks_summary[0]}'
            exc = f'Exceeded: {player_marks_summary[1]}'
            fl = f'Failed: {player_marks_summary[2]}'
            # see if there is a way to bold first line??
            player_marks_text += f'{player_header}\n{exc}\n{fl}\n\n'
    requests.append(f.format_request('player_mark_summary', player_marks_text))

    # Footer
    footer_date_list = game_data[1].split(' ')
    footer_date = footer_date_list[0] + ' ' + footer_date_list[2]
    requests.append(f.format_request('opp_name', school_name))
    requests.append(f.format_request('footer_date', footer_date))
    return requests, game_data[2] + ' Postgame'

from reporting.pregame import PreGameReport
import html_reports.constants as c


def get_marks(cols, all_data, id_str):
    result = []
    for col in cols:
        data = all_data[id_str + col]
        if data['AUC'] >= .7:
            opt_val = data[c.optamt]
            drt = data['direction']
            pct = '%' in col
            if str(opt_val) != 'nan' and drt != 'Flat':
                ou = "O" if drt == "Reverse" else "U"
                val = f'{round(opt_val * 100, 0) if pct else int(round(opt_val, 0))}'
                result_str = ou + val + '%' if pct else ou + val
                result.append(result_str)
            else:
                result.append(c.dash)
        else:
            result.append(c.dash)

    return result


def pregame(pregame_data: PreGameReport, game_data, players):
    color = c.team_colors[pregame_data.opp]
    style = (c.new_style + c.style2.format(color[0]) + c.style3 + c.style4.format(color[1])
             + c.style5)
    gd = game_data[1].split(', ')
    header = c.header.format(game_data[0][2:], gd[0], gd[1])

    ts = pregame_data.summary
    stats_str = (f'{ts["PPG"]} PPG, {ts["RPG"]} RPG, {ts["APG"]} APG, '
                 f'{ts["FG%"] * 100}% FG%, {ts["3P%"] * 100}% 3P%, {ts["FT%"] * 100}% FT%')
    team_details = c.team_details.format(stats_str)

    neu_marks1 = get_marks(c.cols1, pregame_data.team_data, c.opp)
    opp_marks1 = get_marks(c.cols1, pregame_data.team_data, c.school)
    neu_marks2 = get_marks(c.cols2, pregame_data.team_data, c.opp)
    opp_marks2 = get_marks(c.cols2, pregame_data.team_data, c.school)

    neu_mark1 = ''.join([c.benchmark_cell.format(m) for m in neu_marks1])
    opp_abbrev = game_data[2]
    opp_mark1 = ''.join([c.benchmark_cell.format(m) for m in opp_marks1])
    neu_mark2 = ''.join([c.benchmark_cell.format(m) for m in neu_marks2])
    opp_mark2 = ''.join([c.benchmark_cell.format(m) for m in opp_marks2])
    benchmarks = c.benchmarks.format(neu_mark1, opp_abbrev, opp_mark1, neu_mark2, opp_abbrev,
                                     opp_mark2)

    opp_name = game_data[0][2:].strip('Vs. ').strip('@ ').strip('\n')
    p_cols = get_ps(pregame_data.percentiles['Team'])
    opp_p_cols = get_ps(pregame_data.percentiles['Opponent'])
    opp_p = get_p_str(p_cols)
    opp_opp_p = get_p_str(opp_p_cols)

    team_summary = c.team_summary.format(opp_name, opp_p, opp_name, opp_opp_p)

    ws_data = {}
    for p in players:
        ws_data[p[0]] = (pregame_data.win_shares[0][p[0]], p[1:])

    ws_rows = ''
    i = 0
    for player in pregame_data.win_shares[0]:
        data = ws_data[player]
        if i % 2 == 0:
            ws_rows += c.ws_row_1_3.format(player, data[1][0], data[1][1], data[1][2],
                                           str(data[1][3])[:-2],
                                           str(data[0]) + '%')
        else:
            ws_rows += c.ws_row_2_4.format(player, data[1][0], data[1][1], data[1][2],
                                           str(data[1][3])[:-2],
                                           str(data[0]) + '%')
        i += 1

    win_shares = c.win_shares.format(ws_rows)
    player_benchmarks = ''
    for player in pregame_data.player_data:
        data = pregame_data.player_data[player]
        player_bmark = ''
        for stat in data:
            if data[stat]['AUC'] >= .7 and str(data[stat]["optimal amount"]) != 'nan':
                target = c.under if data[stat]['direction'] == 'Normal' else c.over
                amt = int(round(data[stat]["optimal amount"], 0)) if '%' not in stat else int(round(data[stat]["optimal amount"] * 100, 0))
                mark = c.player_benchmark.format(f'{target} {amt} {stat}')
                player_bmark += c.player_benchmark.format(mark)

        if player_bmark != '':
            player_benchmarks += c.player_benchmarks.format(player, player_bmark)

    return (style + header + team_details + benchmarks + team_summary + win_shares
            + player_benchmarks + c.end.format(game_data[1]))


def get_ps(pd):
    p_cols = {p: [] for p in c.percentiles}
    for p in pd:
        pc = 100 - p[1] if p[0] == 'TOV' or p[0] == 'PF' else p[1]
        ps = f'{p[0]}({float(p[2]) * 100})' if '%' in p[0] else f'{p[0]}({p[2]})'
        if pc <= 1:
            p_cols[1].append(ps)
        if pc <= 2:
            p_cols[2].append(ps)
        if pc <= 5:
            p_cols[5].append(ps)
        if pc <= 10:
            p_cols[10].append(ps)
        if pc <= 20:
            p_cols[20].append(ps)
        if pc >= 80:
            p_cols[80].append(ps)
        if pc >= 90:
            p_cols[90].append(ps)
        if pc >= 95:
            p_cols[95].append(ps)
        if pc >= 98:
            p_cols[98].append(ps)
        if pc >= 99:
            p_cols[99].append(ps)

    return p_cols


def get_p_str(p_cols):
    res = ''
    for col in p_cols:
        col_str = ''
        for p in p_cols[col]:
            col_str += c.single_p.format(p)
        res += c.p_row.format(col_str)
    return res

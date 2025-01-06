from bs4 import BeautifulSoup
import requests
import pandas as pd
import database.formatter as f
import scraping.constants as c


# get basic stats and percentiles
def scrape_players(link, opp, names):
    ref_links = get_ref_links(link)
    df = pd.read_html(link)
    # players = df[7]
    players = df[13]
    percentiles = get_percentiles(df[1])
    # summary = get_summary(df[4])
    summary = get_summary(df[7])
    players.sort_values('WS', ascending=False, inplace=True)
    player_info = df[0]
    player_data, win_shares = get_player_data(player_info, players.head(4), ref_links, names)

    return (f.format_players(player_data, opp) if len(player_data) > 0 else None, (win_shares, opp),
            percentiles, summary)


def apply_weight(df):
    df['is_w'] = df['W/L'].apply(lambda x: 1 if 'W' in x else 0)
    df['is_1ot'] = df['W/L'].apply(lambda x: 1 if '1 0T' in x else 0)
    df['is_2ot'] = df['W/L'].apply(lambda x: 1 if '2 OT' in x else 0)
    game_cols = df.columns[2:-3]
    mask1 = df['is_1ot'] == 1
    mask2 = df['is_2ot'] == 1
    df[game_cols] = df[game_cols].astype(float)
    df[game_cols] = df[game_cols].where(~mask1, lambda x: x * .89)
    df[game_cols] = df[game_cols].where(~mask2, lambda x: x * .8)
    df['School/DRB'] = df['School/TRB'] - df['School/ORB']
    df['Opponent/DRB'] = df['Opponent/TRB'] - df['Opponent/ORB']
    df['School/ATO'] = df['School/AST'] / df['School/TOV']
    df['Opponent/ATO'] = df['Opponent/AST'] / df['Opponent/TOV']
    return df.drop(['School/TRB', 'Opponent/TRB'], axis=1)


def get_game_log(link):
    game_log = link[:-5] + c.game_logs
    df = pd.read_html(game_log)[0]
    df.columns = c.cols_to_str(list(df.columns))
    queue = [1, 2]
    df.columns = df.columns.map(lambda x: f'{x}_{queue.pop(0)}' if x == 'Opp' else x)
    df.drop(c.drop_cols, axis=1, inplace=True)
    df.rename(c.rename_cols, axis=1, inplace=True)
    df = df[~df['W/L'].isna()]
    return df[df['W/L'] != 'W/L']


def scrape_team(link):
    df = get_game_log(link)
    df.drop(['Opp_1'], axis=1, inplace=True)
    df = apply_weight(df)
    win = df[df['is_w'] == 1]
    loss = df[df['is_w'] == 0]
    win.drop(['W/L', 'is_w'], axis=1, inplace=True)
    loss.drop(['W/L', 'is_w'], axis=1, inplace=True)
    return win, loss


def get_box_score(link):
    df = get_game_log(link)
    game = df[df['Opp_1'] == 'Northeastern']
    return game.iloc[-1]


def get_post_stats(link, team):
    df = get_game_log(link)
    df = apply_weight(df)
    game = df[df['Opp_1'] == team].index[-1]
    return df.loc[:game - 1]


def get_player_data(info, players, ref_links, names):
    player_data = []
    win_shares = {}
    total_win_shares = players['WS'].sum()
    for i, player in players.iterrows():
        name = players.loc[i, 'Player']
        if name not in names:
            pi = info[info['Player'] == name]
            full_name = name.split(' ')
            height = str(pi['Height'].values[0]).split('-')
            player_data.append((ref_links.get(name),
                                pi['Pos'].values[0],
                                full_name[0],
                                full_name[1],
                                pi['#'].values[0],
                                height[0],
                                height[1],
                                pi['Class'].values[0]))
        win_shares[name] = int((float(players.loc[i, 'WS']) / total_win_shares) * 100)
    return player_data, win_shares


def get_player_stats(players):
    all_stats = {}
    for player in players:
        game_log = player[1][:-5] + c.player_logs
        try:
            df = pd.read_html(game_log)
        except ValueError:
            continue
        if len(df) > 0:
            df = df[0]
            df.drop(c.drop_player_cols, axis=1, inplace=True)
            df.rename({'Unnamed: 6': 'W/L'}, axis=1, inplace=True)
            df.fillna(0, inplace=True)
            win = df[df['W/L'] == "W"].drop(['W/L'], axis=1)
            loss = df[df['W/L'] == "L"].drop(['W/L'], axis=1)
            all_stats[player[0]] = win, loss
    return all_stats


def get_ref_links(link):
    ref_links = {}
    content = requests.get(link).content
    soup = BeautifulSoup(content, 'html.parser')
    roster_table = soup.find('table', attrs={'id': 'roster'})
    player_rows = roster_table.find_all('tr')
    for r in player_rows[1:]:
        player = r.find('th').find('a')
        ref_links[player.text] = 'https://www.sports-reference.com/' + player.get('href')
    return ref_links


def get_percentiles(df):
    result = {
        'Team': [],
        'Opponent': []
    }
    for column in df.columns[3:]:
        p1, p2, = (int(int(df.loc[1, column][:-2]) / 363 * 100),
                   int(int(df.loc[3, column][:-2]) / 363 * 100))
        val1, val2 = df.loc[0, column], df.loc[2, column]

        def add_p(p, side, val):
            if p >= 80 or p <= 20:
                result[side].append((column, p, val))

        add_p(p1, 'Team', val1)
        add_p(100 - p2, 'Opponent', val2)

    return result


def get_summary(df):
    return {'PPG': round(df['PTS'].values[-1] / df['G'].values[-1], 1),
            'RPG': round(df['TRB'].values[-1] / df['G'].values[-1], 1),
            'APG': round(df['AST'].values[-1] / df['G'].values[-1], 1),
            'FG%': df['FG%'].values[-1],
            '3P%': df['3P%'].values[-1],
            'FT%': df['FT%'].values[-1]}


def get_player_game(link):
    df = pd.read_html(link)[0]
    game = df[df['Opp'] == "Northeastern"]
    return df.loc[game.index[0]]

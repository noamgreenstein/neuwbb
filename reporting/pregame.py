import reporting.constants as c
from scraping import scraper
import ml.benchmarks as bm


class PreGameReport:
    def __init__(self, db, game_info):
        self.db = db
        self.win_shares = {}
        self.game_id = game_info[0]
        self.opp = game_info[1]
        self.link = self.db.get_one(c.get_link.format(self.opp))[0]
        self.team_data = {}
        self.player_data = {}
        self.percentiles = {}
        self.summary = {}

    def generate(self):
        self.get_players()
        data = self.get_data()
        player_data = self.get_player_data()
        self.team_data = bm.generate(data)
        for player in player_data:
            try:
                self.player_data[player] = bm.generate(player_data[player])
            except ValueError:
                pass
        self.insert_benchmarks()

    def get_players(self):
        curr_players = [p[0] for p in self.db.get_all(c.get_players.format(self.opp))]
        insert_str, win_shares, self.percentiles, self.summary = scraper.scrape_players(
            self.link, self.opp, curr_players)
        if insert_str:
            self.db.execute_insert(insert_str)
        self.set_win_shares(win_shares)

    def get_data(self):
        return scraper.scrape_team(self.link)

    def get_player_data(self):
        players = self.db.get_all(c.get_player_links.format(self.opp))
        player_data = scraper.get_player_stats(players)
        return player_data

    def insert_benchmarks(self):
        insert_str = ''

        def add_mark(data, target, name):
            if data['AUC'] > .7:
                opt_amt = data['optimal amount']
                drt = data['direction']
                pct = '%' in name
                ato = 'ATO' in name
                if str(opt_amt) != 'nan' and drt != 'Flat':
                    if pct:
                        opt_val = round(opt_amt * 100, 0)
                    elif ato:
                        opt_val = round(opt_amt, 2)
                    else:
                        opt_val = round(opt_amt, 0)

                    return c.mark_value.format(self.game_id, target, drt == "Reverse",
                                                   opt_val,
                                                   name)
            return ''

        for mark in self.team_data:
            insert_str += add_mark(self.team_data[mark], self.opp, mark)

        for player in self.player_data:
            player_id = self.db.get_one(c.get_player_by_name.format(self.opp,
                                                                    player.split(' ')[0],
                                                                    player.split(' ')[1]))[0]
            for mark in self.player_data[player]:
                insert_str += add_mark(self.player_data[player][mark], player_id, mark)

        self.db.execute_insert(c.insert_mark.format(insert_str[:-1]))

    def get_report(self):
        pass

    def get_win_shares(self):
        return self.win_shares

    def set_win_shares(self, win_shares):
        self.win_shares = win_shares

from sklearn.metrics import roc_curve, auc
from sklearn.model_selection import StratifiedKFold
import reporting.constants as c
import numpy as np
from scraping import scraper
from sklearn.linear_model import LogisticRegression


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
        self.team_data = self.get_benchmarks(data)
        for player in player_data:
            self.player_data[player] = self.get_benchmarks(player_data[player])
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

    @staticmethod
    def get_benchmarks(data):
        data_dict = {}
        df1, df2 = data
        df1.fillna(0, inplace=True)
        df2.fillna(0, inplace=True)
        n1, n2 = df1.shape[0], df2.shape[0]

        y = np.concatenate([np.ones(n1), np.zeros(n2)])

        for column in df1.columns:
            total_stat = np.concatenate([df1[column].values, df2[column].values])

            kfold = StratifiedKFold(n_splits=4, shuffle=True, random_state=42)

            x = np.array(total_stat).reshape(-1, 1)
            auc_scores = []
            optimal_thresholds = []
            directions = []
            optimal_nums = []

            # Cross-validation loop
            for train_index, test_index in kfold.split(x, y):
                x_train, x_test = x[train_index], x[test_index]
                y_train, y_test = y[train_index], y[test_index]

                logr = LogisticRegression()
                logr.fit(x_train, y_train)

                y_prob = logr.predict_proba(x_test)[:, 1]
                fpr, tpr, thresholds = roc_curve(y_test, y_prob)
                auc_scores.append(auc(fpr, tpr))

                optimal_idx = np.argmax(tpr - fpr)
                optimal_threshold = thresholds[optimal_idx]
                optimal_thresholds.append(optimal_threshold)

                beta_0 = logr.intercept_[0]
                beta_1 = logr.coef_[0][0]
                direction = 'Normal' if beta_1 > 0 else 'Reverse' if beta_1 < 0 else 'Flat'
                directions.append(direction)

                optimal_nums.append((np.log(
                    optimal_threshold / (1 - optimal_threshold)) - beta_0) / beta_1)

            average_auc = np.mean(auc_scores)
            most_common_direction = max(set(directions), key=directions.count)
            optimal_stat = np.mean(optimal_nums)

            data_dict[column] = {
                'AUC': average_auc,
                'optimal amount': optimal_stat,
                'direction': most_common_direction
            }

        return data_dict

    def insert_benchmarks(self):
        insert_str = ''

        def add_mark(data, target, name):
            if data['AUC'] > .7:
                opt_val = data['optimal amount']
                drt = data['direction']
                pct = '%' in data
                if str(opt_val) != 'nan' and drt != 'Flat':
                    return c.mark_value.format(self.game_id, target, drt == "Reverse",
                                               round(opt_val * 100, 0) if pct else int(
                                                   round(opt_val, 0)),
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

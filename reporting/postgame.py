import reporting.constants as c
import scraping.scraper as s


class PostGameReport:
    def __init__(self, db, game_info):
        self.db = db
        self.game_id = game_info[0]
        self.opp = game_info[1]
        self.link = self.db.get_one(c.get_link.format(self.opp))[0]
        self.opp_ref = self.db.get_one(c.get_ref_name.format(self.opp))[0]
        self.players = self.db.get_all(c.get_players_id.format(self.opp))
        self.model = {}
        self.box_score = {}
        self.opp_stats = {}
        self.neu_stats = {}
        self.player_stats = {}
        self.expected_stats = {}
        self.benchmarks = self.db.get_all(c.get_marks.format(self.game_id))

    def generate(self):
        self.box_score = s.get_box_score(self.link)
        self.opp_stats = s.get_post_stats(self.link, 'Northeastern')
        self.neu_stats = s.get_post_stats(c.neu_link, self.opp_ref)
        for player in self.players:
            self.player_stats[player[1]] = s.get_player_game(player[3])
        self.box_score['Opponent/DRB'] = int(self.box_score['Opponent/TRB']) - int(self.box_score['Opponent/ORB'])
        self.box_score['School/DRB'] = int(self.box_score['School/TRB']) - int(self.box_score['School/ORB'])
        self.box_score['Opponent/ATO'] = float(self.box_score['Opponent/AST']) / int(self.box_score['Opponent/TOV'])
        self.box_score['School/ATO'] = float(self.box_score['School/AST']) / float(self.box_score['School/TOV'])
class Game:
    def __init__(self, title):
        self.title = title

    def results(self):
        return [result for result in Result.all if result.game == self]
    def players(self):
        return list(set([result.player for result in Result.all if result.game == self]))
    def average_score(self, player):
        total_score = sum([result.score for result in Result.all if result.game == self and result.player == player])
        num_times_played = sum([1 for result in Result.all if result.game == self and result.player == player])
        return total_score / num_times_played
    
    @property
    def title(self):
        return self._title
    @title.setter
    def title(self, title):
        if hasattr(self, "title"):
            raise Exception("Cannot assign title after game has been created.")
        elif type(title) != str:
            raise Exception("Title must be a string!")
        elif len(title) < 1:
            raise Exception("Title must be longer than 0 characters.")
        else:
            self._title = title

class Player:
    def __init__(self, username):
        self.username = username

    def results(self):
        return [result for result in Result.all if result.player == self]
    def games_played(self):
        return list(set([result.game for result in Result.all if result.player == self]))
    def played_game(self, game):
        for result in Result.all:
            if result.player == self and result.game == game:
                return True
        return False
    def num_times_played(self, game):
        count = 0
        for result in Result.all:
            if result.player == self and result.game == game:
                count += 1
        return count
    
    @classmethod
    def highest_scored(cls, game):
        player_averages_for_game = {}

        for result in Result.all:
            if result.game == game:
                if result.player.username not in player_averages_for_game:
                    player_averages_for_game[result.player.username] = []
                player_averages_for_game[result.player.username].append(result.score)
        for key in player_averages_for_game:
            player_averages_for_game[key] = sum(player_averages_for_game[key]) / len(player_averages_for_game[key])

        player_averages_for_game = sorted(player_averages_for_game, key = lambda key: player_averages_for_game[key], reverse = True)
        max_player = player_averages_for_game[0]

        for result in Result.all:
            if result.game == game and result.player.username == max_player:
                max_player = result.player

        return max_player or None

    @property
    def username(self):
        return self._username
    @username.setter
    def username(self, name):
        if isinstance(name, str) and 2 <= len(name) <= 16:
            self._username = name
        else:
            raise Exception("Your username needs to be between 2 and 16 characters.")
        
class Result:
    all = []

    def __init__(self, player, game, score):
        self.player = player
        self.game = game
        self.score = score
        Result.all.append(self)

    @property
    def player(self):
        return self._player
    @player.setter
    def player(self, player):
        if not isinstance(player, Player):
            raise Exception("Must be of type Player.")
        else:
            self._player = player

    @property
    def game(self):
        return self._game
    @game.setter
    def game(self, game):
        if not isinstance(game, Game):
            raise Exception("Must be of type Game.")
        else:
            self._game = game

    @property
    def score(self):
        return self._score
    @score.setter
    def score(self, score):
        if hasattr(self, "score"):
            raise Exception("Cannot set score after game has finished.")
        elif type(score) != int:
            raise Exception("Score must be an integer.")
        elif 1 > score > 5000:
            raise Exception("Score must be between 1 and 5000.")
        else:
            self._score = score

    

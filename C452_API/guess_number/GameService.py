# "Bulls and Cows". In each game, a 4-digit number is generated where every digit is different.
# For each round, the user guesses a number and is told the exact and partial digit matches.
# MATCH = correct digit in the correct position.
# PARTIAL MATCH = correct digit but in the wrong position.
# WIN = 4 MATCHES


# "begin" - POST – Starts a game, generates an answer, and sets the correct status. Should return a 201 CREATED message as well as the created gameId.
# "guess" – POST – Makes a guess by passing the guess and gameId in as JSON. The program must calculate the results of the guess and mark the game finished if the guess is correct. It returns the Round object with the results filled in.
# "game" – GET – Returns a list of all games. Be sure in-progress games do not display their answer.
# "game/{gameId}" - GET – Returns a specific game based on ID. Be sure in-progress games do not display their answer.
# "rounds/{gameId} – GET – Returns a list of rounds for the specified game sorted by time.
# You should include a Service layer to manage the game rules, such as generating initial answers for a game and calculating the results of a guess.

import random
from database import new_game, insert_round, getGameById, get_db_games, win_game, get_rounds_of_game
class GameService:

    @staticmethod
    def generate_answer():
        """ Generates a random 4-digit answer with unique digits. """
        digits = list('0123456789')
        random.shuffle(digits)
        return ''.join(digits[:4])

    @classmethod
    def start_game(cls):
        """ 
        Starts a new game, generates an answer, and sets the correct status.
    
        Returns:
            int: The ID of the created game.
        """
        answer = cls.generate_answer()
        new_game_info = {
            'answer': answer,
            'status': 'in_progress'
        }
        game_id = new_game(new_game_info)
        print(game_id)
        return game_id

    @classmethod
    def record_round(cls, game_id, guess):
        guess_result = cls.calculate_guess_result(cls,game_id, guess)

        return guess_result

    @staticmethod 
    def get_game_by_id(game_id):
        ans = getGameById(game_id)
        return ans
        
    
    @staticmethod
    def calculate_guess_result(cls, game_id, guess):
        game = cls.get_game_by_id(game_id)
        answer = game['answer']

        guess_str = str(guess)
        answer_str = str(answer)

        # zip() methid pairs up the characters at the same index 
        exact = sum(1 for g, a in zip(guess_str, answer_str) if g == a)
        partial = sum(1 for g in guess_str if g in answer_str) - exact

        round_info = {
            'partial': partial,
            'exact': exact,
            'guess': guess_str,
        }
        
        res = insert_round(round_info, game_id)

        round_object = {
            'round_id': res[0],
            'game_id': res[1],
            'guess': res[2],
            'partial_matches': res[3],
            'exact_matches': res[4],
            'guess_timestamp': res[5]
        }

        if res[4] == 4:
            win_game(game_id)
        print(round_object)
        return round_object
    

    @staticmethod
    def get_all_games():
        games = get_db_games()
        return games

    @staticmethod 
    def get_all_rounds(game_id):
        ans = get_rounds_of_game(game_id)
        return ans
        

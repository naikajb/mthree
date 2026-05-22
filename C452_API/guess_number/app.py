from flask import Flask, jsonify, request, Response
import mysql.connector
import json
# import our database connection
from GameService import GameService
from database import initialize_database

app = Flask(__name__)
app.json.sort_keys = False



@app.route('/')
def home():
    text = "<h2>Welcome to the Bulls and Cows API</h2>"
    text += "<p>Use the following endpoints to play the game:</p>"
    text += "<ul>"
    text += "<li><strong>POST /begin</strong> - Start a new game</li>"
    text += "<li><strong>POST /guess</strong> - Make a guess by passing the guess and gameId in JSON</li>"
    text += "<li><strong>GET /game</strong> - Get a list of all games (in-progress games do not display their answer)</li>"
    text += "<li><strong>GET /game/{gameId}</strong> - Get a specific game by ID (in-progress games do not display their answer)</li>"
    text += "<li><strong>GET /rounds/{gameId}</strong> - Get a list of rounds for the specified game sorted by time</li>"
    text += "</ul>"
    return text

@app.route('/begin', methods=['POST'])
def begin_game():
    # call game start from GameService
    try:
        game_id = GameService.start_game()
        
        return jsonify({
        "message": "Game created successfully",
        "gameId": game_id
    }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/guess', methods=['POST'])
def guess():
    """ 
        Passes the guess and game ID in as JSON
    
        RETURNS: Round object with results filled in
    """
    data = request.get_json(force=True, silent=True)
    game_id, guess = data['gameId'], data['guess']
    
    this_round = GameService.record_round(game_id, guess)
    return jsonify({'round': this_round, 'message': "The round was registered succesfully"}), 200


@app.route('/games', methods=['GET'])
def get_all_games():
    games = GameService.get_all_games()
    return Response(
        json.dumps(games, sort_keys=False),
        mimetype = 'application/json'
    ), 200

@app.route("/game/<int:gameId>")
def get_game_by_id(gameId):
    game = GameService.get_game_by_id(gameId)
    if game is None: 
        return jsonify({"error": "No game with gameId \'{gameId}\'was found"}), 500
    else: 
        return jsonify({"game": game, "message": 'Game with ID \'{gameId}\' was found'}), 200


@app.route('/rounds/<int:gameId>')
def get_all_rounds(gameId):
    rounds = GameService.get_all_rounds(gameId)

    if rounds is None: 
        return jsonify({"error": "No game with gameId \'{gameId}\' was found"}), 500
    else: 
        return jsonify({"ALL Rounds": rounds, "message": 'Game with ID  \'{gameId}\'  was found'}), 200
    return


if __name__ == '__main__':
    initialize_database()
    app.run(debug=True)
    
    
    
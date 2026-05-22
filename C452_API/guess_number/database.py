import mysql.connector


db_config = {
    'host': 'localhost',
    'database': 'BullsAndCowsDB',
    'user': 'root'
}

def get_db_connection():
    """ returns a connection to the database. """
    return mysql.connector.connect(**db_config)

def initialize_database():
    """ Initializes the db connection and creates the necessary tables if they do not exist. """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS games (
        game_id INT AUTO_INCREMENT PRIMARY KEY,
        answer VARCHAR(4) NOT NULL,
        status ENUM('in_progress', 'finished') DEFAULT 'in_progress'
    )""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS rounds (
        round_id INT AUTO_INCREMENT PRIMARY KEY,
        game_id INT NOT NULL,
        guess VARCHAR(4) NOT NULL,
        partial_matches INT NOT NULL,
        exact_matches INT NOT NULL,
        guess_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (game_id) REFERENCES games(game_id)
    )""")
    conn.commit()
    cursor.close()
    conn.close()

    print("Database has been initialized")


def new_game(game):
    """ Insert new game into the DB
    Args:
        game (dict): A dictionary containing the game details (answer and status).
    Returns:
        int: The ID of the newly created game.
    """
    answer, status = game['answer'], game['status']
    
    conn = get_db_connection()
    cursor = conn.cursor()

    insert_query = "INSERT INTO games (answer, status) VALUES (%s, %s)"
    cursor.execute(insert_query, (answer,status))
    
    conn.commit()

    game_id = cursor.lastrowid

    
    cursor.close()
    conn.close()
    return game_id


def insert_round(round_info, game_id):
    """ 
        inserts the players guess into the round table and updates the game info 
        RETURNS the round info
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = "INSERT INTO rounds (game_id, guess, partial_matches, exact_matches) VALUES (%s, %s, %s, %s)"

        partial = round_info['partial']
        exact = round_info['exact']
        guess = round_info['guess']

        cursor.execute(query, (game_id, guess, partial, exact))
        conn.commit()

        last_id = cursor.lastrowid

        cursor.execute("SELECT * FROM rounds WHERE round_id = %s", (last_id,))
        round_object = cursor.fetchone()
        cursor.close()
        conn.close()
        return round_object
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

    
def getGameById(game_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = "SELECT game_id, answer, status FROM games WHERE game_id = %s"
        cursor.execute(query, (game_id,))
        row = cursor.fetchone()
        if row:
            return {'game_id': row[0], 'answer': row[1], 'status' :row[2]}
        return None
    finally:
        cursor.close()
        conn.close()
    
def get_db_games():
    conn = get_db_connection()
    cursor = conn.cursor()
    games = []

    try: 
        cursor.execute("SELECT * FROM games")
        for row in cursor:
            answer = 'hidden' if row[2] == 'in_progress' else row[1]

            game = {
                'game_id': row[0],
                'answer': answer,
                'status': row[2]
            }
            games.append(game)
    except Exception as e:
        print(f'error fetching games: {e}')
    
    return games

def win_game(game_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("UPDATE games SET status = 'finished' WHERE game_id = %s", (game_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return

def get_rounds_of_game(game_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    rounds = []

    try: 
        cursor.execute("SELECT * FROM rounds WHERE game_id = %s ORDER BY guess_timestamp DESC;", (game_id,))
        for row in cursor:
            round = {
                'round_id': row[0],
                'game_id': row[1],
                'guess': row[2],
                'partial_matches': row[3],
                'exact_matches': row[4],
                'guess_timestamp': row[5]
            }
            rounds.append(round)
    except Exception as e:
        print(f'error fetching rounds: {e}')

    cursor.close()
    conn.close()
    return rounds



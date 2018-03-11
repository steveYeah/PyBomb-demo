import os

from flask import Flask, render_template, request
from pybomb import GamesClient, GameClient


app = Flask(__name__)
app.config['PYBOMB_KEY'] = os.environ.get("PYBOMB_KEY")


@app.route('/', methods=('GET', 'POST'))
def main():
    if request.method == 'GET':
        return render_template('home.html')

    games_client = GamesClient(app.config['PYBOMB_KEY'])
    search_title = request.form['search_title']
    games = games_client.quick_search(search_title)

    game_results = [
        {
            'id': game['id'],
            'title': game['name'],
            'thumbnail': game['image']['icon_url'],
        } for game in games.results
    ]

    return render_template(
        'home.html',
        search_title=search_title,
        games=game_results,
    )


@app.route('/game/<int:game_id>', methods=('GET',))
def game(game_id):
    game_client = GameClient(app.config['PYBOMB_KEY'])
    game = game_client.fetch(game_id)

    game_result = {
        'id': game.results['id'],
        'name': game.results['name'],
        'description': game.results['deck'],
        'image': game.results['image']['small_url'],
    }

    return render_template(
        'game.html',
        game=game_result,
    )

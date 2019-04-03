import os
from datetime import datetime

from flask import Flask, render_template, request
from pybomb import GamesClient, GameClient


app = Flask(__name__)
app.config["PYBOMB_KEY"] = os.environ.get("PYBOMB_KEY")


@app.route("/", methods=("GET", "POST"))
def main():
    if request.method == "GET":
        return render_template("home.html")

    games_client = GamesClient(app.config["PYBOMB_KEY"])
    search_title = request.form["search_title"]
    games = games_client.quick_search(search_title)

    game_results = [
        {
            "id": game["id"],
            "title": game["name"],
            "thumbnail": game["image"]["icon_url"],
        }
        for game in games.results
    ]

    return render_template("home.html", search_title=search_title, games=game_results)


@app.route("/game/<int:game_id>", methods=("GET",))
def game(game_id):
    game_client = GameClient(app.config["PYBOMB_KEY"])
    game = game_client.fetch(game_id)

    if game.results["original_release_date"]:
        release_date = datetime.strptime(
            game.results["original_release_date"], "%Y-%m-%d %H:%M:%S"
        ).strftime("%d/%m/%Y")
    else:
        release_date = "Unreleased"

    if game.results.get("developers"):
        developer = game.results.get("developers")[0]["name"]
    else:
        developer = "Unknown"

    if game.results.get("publishers"):
        publisher = game.results.get("publishers")[0]["name"]
    else:
        publisher = "Unknown"

    game_result = {
        "id": game.results["id"],
        "name": game.results["name"],
        "release_date": release_date,
        "developer": developer,
        "publisher": publisher,
        "deck": game.results["deck"],
        "image": game.results["image"]["small_url"],
    }

    return render_template("game.html", game=game_result)


@app.route("/game/<int:game_id>/details", methods=("GET",))
def game_details(game_id):
    game_client = GameClient(app.config["PYBOMB_KEY"])
    game = game_client.fetch(game_id)

    if game.results["description"]:
        description = game.results["description"]
    else:
        description = "Sorry, we couldn't find any more details"

    game_details = {
        "id": game.results["id"],
        "details": description,
        "name": game.results["name"],
    }

    return render_template("game_details.html", game=game_details)

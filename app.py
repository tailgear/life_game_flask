from flask import Flask, render_template
from game_of_life import GameOfLife

app = Flask(__name__)

@app.route('/')
def index():
    GameOfLife(50, 50)
    return render_template('index.html')

@app.route('/live')
def live():
    game = GameOfLife()
    game.next_generation()
    return render_template('live.html', game=game)


if __name__ == '__main__':
    app.run('localhost', 5000, True)
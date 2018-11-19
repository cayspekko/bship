from flask import Flask, request, redirect, url_for, render_template, flash, session
import bshipbe
app = Flask(__name__)
app.config["DEBUG"] = True
app.secret_key = "super secret key"

@app.route('/board/<board_id>/reveal')
def get_board(board_id):
	if board_id == session.get('board'):
		board = bshipbe.print_ships(board_id)
		return render_template("board.html", board=board)
	else:
		return redirect(url_for('start_board', board_id=board_id))

@app.route('/board/<board_id>')
def start_board(board_id):
	message = None
	if request.args.get('message'):
		message = request.args['message']
	board = bshipbe.print_board(board_id)
	return render_template("start_board.html", board=board, board_id=board_id, message=message)

@app.route('/board/<board_id>/attack', methods=['POST'])
def attack_board(board_id):
	message = None
	if request.method == "POST":
		coord = request.form['coord']
		try:
			my_board_id = session["board"]
			message = bshipbe.attack(board_id, my_board_id, coord)
		except ValueError as e:
			message = e
		except KeyError:
			message = "You can't attack until you've upload a board"
	return redirect(url_for('start_board', board_id=board_id, message=message))

@app.route('/board/create', methods=['PUT', 'POST'])
def create_board():
	print('-->', 'test')
	if request.method == "POST":
		board = request.form['board']
		ships = bshipbe.parse_board(board)
	else:
		raise NotImplemented()
	board_url = bshipbe.load_board(ships)
	session["board"] = board_url
	print('-->', board_url)
	return redirect(url_for('get_board', board_id=board_url))

@app.route('/board/upload')
def upload_board():
	return render_template("upload_board.html")

@app.route('/board')
def list_boards():
	boards = bshipbe.list_boards()
	return render_template("list_boards.html", boards=boards)

if __name__ == "__main__":
	app.run()
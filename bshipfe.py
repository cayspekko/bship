from flask import Flask, request, redirect, url_for, render_template, flash, session
import bshipbe
app = Flask(__name__)
app.config["DEBUG"] = True
app.secret_key = "super secret key"


def count_coord():
	for i in range(100):
		r = int(i/10)
		c = i % 10
		yield "%s%s" % (chr(ord('a') + r), c + 1)

@app.route('/board/<board_id>/reveal/')
def get_board(board_id):
	if board_id == session.get('board'):
		board = bshipbe.print_ships(board_id)
		return render_template("board.html", board=board, board_id=board_id)
	else:
		return redirect(url_for('start_board', board_id=board_id))

@app.route('/board/<board_id>/', methods=['POST', 'GET'])
def start_board(board_id):
	if request.method == "POST":
		password = request.form['password']
		rval = bshipbe.login_board(board_id, password)
		if rval:
			session['board'] = board_id

	message = None
	if request.args.get('message'):
		message = request.args['message']
	# board = bshipbe.print_board(board_id)
	hits, misses = bshipbe.get_attacks(board_id)
	lines = ['  1 2 3 4 5 6 7 8 9 10']
	cc = count_coord()
	for row in range(10):
		line = chr(ord('a') + row)
		for col in range(10):
			coord = next(cc)
			if [row, col] in hits:
				line += ' x'
			elif [row, col] in misses:
				line += ' o'
			else:
				if board_id != session.get('board'):
					line += ' <a href=%s style="text-decoration: none">.</a>' % url_for("start_board", board_id=board_id, coord=coord)
				else:
					line += ' .'
		lines.append(line)
	board = '\n'.join(lines)
	challenger = bshipbe.get_challenger(board_id)
	turn = bshipbe.get_turn(board_id)
	return render_template("start_board.html", board=board, board_id=board_id, challenger=challenger, turn=turn, message=message)

@app.route('/board/<board_id>/attack/', methods=['POST'])
def attack_board(board_id):
	message = None
	if request.method == "POST":
		coord = request.form['coord'][:3].lower()
		try:
			my_board_id = session["board"]
			message = bshipbe.attack(board_id, my_board_id, coord)
		except ValueError as e:
			message = e
		except KeyError:
			message = "You can't attack until you've upload a board"
	return redirect(url_for('start_board', board_id=board_id, message=message))

@app.route('/board/create/', methods=['PUT', 'POST'])
def create_board():
	if request.method == "POST":
		board = request.form['board']
		ships = bshipbe.parse_board(board)
		name = request.form.get('name')
		password = request.form.get('password')
	else:
		raise NotImplemented()

	board_url = bshipbe.load_board(ships)
	session["board"] = board_url
	bshipbe.set_attributes(board_url, name, password)
	return redirect(url_for('get_board', board_id=board_url))

@app.route('/board/upload/')
def upload_board():
	gen_board = None
	if request.args.get('random'):
		gen_board = bshipbe.random_board_file()
	return render_template("upload_board.html", gen_board=gen_board)

@app.route('/board/')
def list_boards():
	filter = request.args.get('name')
	boards = bshipbe.list_boards(filter)
	my_board = session.get('board')
	return render_template("list_boards.html", boards=boards, my_board=my_board)

@app.route('/board/<board_id>/logout')
def logout_board(board_id):
	try:
		del session['board']
	except KeyError:
		pass
	return redirect(url_for("start_board", board_id=board_id))

if __name__ == "__main__":
	app.run()
	# next(count_coord())
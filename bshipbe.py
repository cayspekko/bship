import pickledb
import uuid

bshipdb = None
valid = {'a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 'a9', 'a10', 'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8',
         'b9', 'b10', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'c10', 'd1', 'd2', 'd3', 'd4', 'd5', 'd6',
         'd7', 'd8', 'd9', 'd10', 'e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8', 'e9', 'e10', 'f1', 'f2', 'f3', 'f4',
         'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'g1', 'g2', 'g3', 'g4', 'g5', 'g6', 'g7', 'g8', 'g9', 'g10', 'h1', 'h2',
         'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9', 'h10', 'i1', 'i2', 'i3', 'i4', 'i5', 'i6', 'i7', 'i8', 'i9', 'i10',
         'j1', 'j2', 'j3', 'j4', 'j5', 'j6', 'j7', 'j8', 'j9', 'j10'}

def lazy(fn):
	global bshipdb
	if not bshipdb:
		bshipdb = pickledb.load('bshipdb.db', True)
	return fn

def generate_board_url():
	return uuid.uuid4().hex

@lazy
def load_board(ships):
	bd = {"ships": ships, "hits": [], "misses": []}
	board_url = generate_board_url()
	bshipdb.set(board_url, bd)
	return board_url

@lazy
def print_board(board_url):
	board = bshipdb.get(board_url)
	misses = board['misses']
	hits = board['hits']

	lines = ["  1 2 3 4 5 6 7 8 9 10"]
	for row in range(10):
		l = chr(ord("a") + row)
		for col in range(10):
			if [row, col] in misses:
				l += ' o'
			elif [row, col] in hits:
				l += ' x'
			else:
				l += ' .'
		lines.append(l)
	print("\n".join(lines))
	return "\n".join(lines)

@lazy
def print_ships(board_url):
	print('-->board_url', board_url)
	board = bshipdb.get(board_url)
	ships = board['ships']
	print('-->ships', ships)
	lines = ["  1 2 3 4 5 6 7 8 9 10"]
	for row in range(10):
		l = chr(ord("a") + row)
		for col in range(10):
			if [row, col] in ships:
				l += ' x'
			else:
				l += ' .'
		lines.append(l)
	print("\n".join(lines))
	return "\n".join(lines)

def parse_coord(coord):
	return [ord(coord[0]) - ord('a'), int(coord[1:]) - 1]

@lazy
def attack(board_url, my_board_id, unparsed_coord):
	if board_url == my_board_id:
		raise ValueError("can't attack your own board")

	if unparsed_coord not in valid:
		raise ValueError(str(unparsed_coord) + " seems invalid")

	board = bshipdb.get(board_url)
	if board.get('challenger') and board['challenger'] != my_board_id:
		raise ValueError("This board %s is already under attack by someone else!" % board_url)

	if board.get('turn') and board['turn'] != my_board_id:
		raise ValueError("It's not your turn!")
	else:
		board['turn'] = board_url

	c = parse_coord(unparsed_coord)
	ships = board['ships']
	hits = board['hits']
	misses = board['misses']

	if c in ships:
		if c not in hits:
			hits.append(c)
		print("HIT!")
		message = "hit"
		print('-->hit ships', hits, ships)
		if all(ship in hits for ship in ships):
			print("YOU WIN")
			message = "win"
	else:
		print("MISS!")
		message = "miss"
		if c not in misses:
			misses.append(c)
	bshipdb.set(board_url, board)

	# release my turn
	my_board = bshipdb.get(my_board_id)
	my_board['turn'] = board_url
	bshipdb.set(my_board_id, my_board)

	return message

@lazy
def attack_by_name(name, unparsed_coord):
	bshipdb.get(name)

def parse_board(board):
	ships = []
	lines = board.split('\n')[0:10]
	for row in range(10):
		l = lines[row]
		for col in range(10):
			if l[col] == 'x':
				ships.append([row, col])
			elif l[col] != '.':
				raise ValueError(str(l[col]) + " seems invalid")
	return ships

@lazy
def list_boards():
	return bshipdb.getall()

if __name__ == "__main__":
	import sys
	fname = sys.argv[1]
	ships = []
	with open(fname) as f:
		for row in range(10):
			l = f.readline()
			for col in range(10):
				if l[col] != '.':
					ships.append([row, col])
	board_url = load_board(ships)
	print(board_url)
	print_ships(board_url)
	print_board(board_url)

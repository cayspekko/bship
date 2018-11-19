import sys
import os

ships = set()
hits = set()
misses = set()


def usage():
	print("USAGE:")
	print(os.path.basename(sys.argv[0]), "[filename]")


def parse_coord(coord):
	return ord(coord[0]) - ord('a'), int(coord[1:]) - 1

def print_board():
	print("  1 2 3 4 5 6 7 8 9 10")
	for row in range(10):
		l = chr(ord("a") + row)
		for col in range(10):
			if (row, col) in misses:
				l += ' o'
			elif (row, col) in hits:
				l += ' x'
			else:
				l += ' .'
		print(l)


if __name__ == "__main__":
	try:
		fname = sys.argv[1]
		with open(fname) as f:
			for row in range(10):
				l = f.readline()
				for col in range(10):
					if l[col] != '.':
						ships.add((row, col))

	except IndexError:
		usage()
	except OSError:
		print("Invalid file format")
	else:
		print(ships)
		while True:
			i = input('-->')
			if i == "quit":
				break
			if len(i) == 2 or len(i) == 3:
				try:
					c = parse_coord(i)
				except ValueError:
					print(i, "is invalid")
					continue
				print(c)
				if c in ships:
					hits.add(c)
					print("HIT!")
					print('-->hits shps', hits, ships)
					if hits == ships:
						print("YOU WIN")
						break
				else:
					print("MISS!")
					misses.add(c)
			if i == 'p':
				print_board()


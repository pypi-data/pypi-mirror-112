import sys
import inspect
import readchar
import readline as rl
import argparse
import datetime
from pathlib import Path
from shutil import copytree, rmtree

from vinca.lib.classes import Card
from vinca.lib import ansi
from vinca.lib import filter
from vinca.generators import generate, GENERATORS_DICT

# TODO: intelligent scrollback for reviewers and editors
# how? intelligent parameterization
# TODO: make functions specify the parameters they need and 
# feed them this explicitly á la FILTER

TODAY = datetime.date.today()

PIPE_IN = not sys.stdin.isatty()
PIPE_OUT = not sys.stdout.isatty()
QUIT_KEYS = ['q', readchar.key.ESC, '\n', '\r']

vinca_path = Path(__file__).parent 
cards_path = vinca_path / 'cards'
ALL_CARDS = [Card(int(id.name)) for id in cards_path.iterdir()]
ALL_TAGS = [tag for card in ALL_CARDS for tag in card.tags] # TODO: cache

# ARGUMENT PARSING
parser = argparse.ArgumentParser(usage=argparse.SUPPRESS, epilog='Use -h to see help for any command. Visit the manual for usage examples.')
subparsers = parser.add_subparsers(metavar='')
def card_type(arg):
	id = int(arg.split()[0])  # grab the first field of the argument
	return Card(id)
def date_type(s):
	if s[s[0] in ['+','-']:].isdigit():
		return TODAY + int(arg) * DAY
	try:
		return datetime.datetime.strptime(s, '%Y-%m-%d').date()
	except ValueError:
		raise argparse.ArgumentTypeError(f'''\n\n
			Invalid Date: {s}. Valid dates are:
			1) -7		(one week ago)
			2) 2021-06-03	(June 3rd)''')
def arg(*names_or_flags, **kwargs):
	return names_or_flags, kwargs
CARDS = arg('cards',nargs='*',type=card_type, default=ALL_CARDS)
CARD = arg('card',type=card_type)
OPTIONAL_CARD = arg('card', nargs='?', type=card_type)
OPTIONAL_CARDS = arg('--cards',nargs='*',type=card_type,default=ALL_CARDS)
OPTIONAL_CARDS_DEFAULT_NONE = arg('--cards',nargs='*',type=card_type,default=[])
def subcommand(*subparser_args, parent=subparsers, alias='', name=None):
	def decorator(func, alias=alias, name=name):
		name = name if name else func.__name__
		description = func.__doc__
		aliases = [alias] if alias else []
		parser = parent.add_parser(name, help='', description=description, aliases=aliases,
		                           usage=argparse.SUPPRESS)
		for args, kwargs in subparser_args:
			parser.add_argument(*args, **kwargs)
		parser.set_defaults(func=func)
		return func
	return decorator

@subcommand(arg('-t','--default_tags', nargs='+', default=[]), alias='a')
def add(args): 
	ansi.hide_cursor()
	print(*[f'{key}\t{generator}' for key, generator in GENERATORS_DICT.items()],sep='\n')
	k = readchar.readchar()
	if k not in GENERATORS_DICT: return
	args.generator = GENERATORS_DICT[k]
	args.cards = generate(args)
	ansi.up_line(len(GENERATORS_DICT) + 2)
	ansi.clear_to_end()
	browse(args)

@subcommand(OPTIONAL_CARD, OPTIONAL_CARDS, alias='s')
def statistics(args):
	if args.card:
		card = args.card
		print(f'\nCard #{card.id}')
		print(str(card))
		print(f'Tags: {" ".join(card.tags)}')
		print(f'Due: {card.due_date}')
		print('Date\t\tTime\tGrade')
		print(*[f'{date}\t{time}\t{grade}' for date, time, grade in card.history],sep='\n',end='')
		lines = 5+len(card.history)
	elif args.cards:
		due_cards = filter.filter(args.cards, due_only=True)
		new_cards = filter.filter(args.cards, new_only=True)
		print('Total', len(args.cards), sep='\t')
		print('Due', len(due_cards), sep='\t')
		print('New', len(new_cards), sep='\t')
		lines = 3
	if args.scrollback:
		ansi.up_line(lines)
		ansi.hide_cursor()

@subcommand(CARD,alias='e')
def edit(args):
	''' edit a single card '''
	args.card.edit()

@subcommand(CARD,alias='E')
def edit_metadata(args):
	''' edit the metadata of a card '''
	args.card.edit_metadata()

@subcommand(OPTIONAL_CARD, OPTIONAL_CARDS_DEFAULT_NONE, alias='x')
def delete(args):
	if args.card:
		args.card.deleted = not args.card.deleted
	elif args.cards:
		for card in args.cards:
			card.deleted = not card.deleted

@subcommand(CARDS, alias='r')
def review(args):
	if args.card:
		args.card.review()
		args.card.schedule()
	elif args.cards:
		args.cards = filter.filter(args.cards, due_only = True)
		if not args.cards:
			print('No cards due.')
			return
		browse(args, reviewing = True)

@subcommand(arg('tag'), OPTIONAL_CARD, OPTIONAL_CARDS_DEFAULT_NONE)
def add_tag(args):
	for card in [args.card] if args.card else args.cards:
		card.tags += [args.tag]

@subcommand(arg('tag'), OPTIONAL_CARD, OPTIONAL_CARDS_DEFAULT_NONE)
def remove_tag(args):
	for card in [args.card] if args.card else args.cards:
		if args.tag in card.tags:
			card.tags.remove(args.tag)
		# TODO do this with set removal
		card.save_metadata()

@subcommand(OPTIONAL_CARD, OPTIONAL_CARDS_DEFAULT_NONE, alias='t')
def edit_tags(args):
	def complete(text, state):
		for tag in ALL_TAGS:
			if tag.startswith(text):
				if not state:
					return tag
				else:
					state -= 1
	rl.parse_and_bind('tab: complete')
	rl.set_completer(complete)

	if args.card:
		pass #TODO lineedit tags with tab complete
		tags = ' '.join(args.card.tags)
		rl.set_startup_hook(lambda: rl.insert_text(tags))
		args.card.tags = input('tags: ').split()
		lines = 1
		rl.set_startup_hook()
	elif args.cards:
		tags_add = input('tags to add: ').split()
		tags_remove = input('tags to remove: ').split()
		lines = 2
		for tag in tags_add:
			args.tag = tag
			add_tag(args)
		for tag in tags_remove:
			args.tag = tag
			remove_tag(args)
	
	rl.set_completer()

	if args.scrollback:
		ansi.up_line(lines)


CMD_DICT = {'r': review, 'R': review,
	    's': statistics, 'S': statistics,
	    'x': delete, 'X': delete,
	    'e': edit, 'E': edit_metadata,
	    't': edit_tags, 'T': edit_tags}
@subcommand(arg('--cards',nargs='*',type=card_type,default=filter.filter(ALL_CARDS)), arg('-t','--default_tags', nargs='+', default=[]), alias='b')
def browse(args, reviewing = False):
	''' Use J and K to move up and down. In general a lowercase letter will act on the selected card while a capital letter will act upon all cards. Use the following hotkeys in browse mode: r, x, s, e, t'''
	args.scrollback = True
	cards = args.cards
	if not cards:
		print('no cards')
		return
	FRAME_WIDTH = 10  # TODO better width?
	STATUS_BAR = len(cards) > FRAME_WIDTH
	# TODO max frame of ten cards
	n = len(cards); sel = 0

	def quit():
		ansi.show_cursor()
		ansi.clear_to_end()
		exit()
	def draw_browser(frame):
		ansi.hide_cursor()
		ansi.line_wrap_off()

		if STATUS_BAR:
			ansi.light()
			print(f'{sel+1} of {len(cards)}')
			ansi.reset()
		for i, card in enumerate(cards[frame:frame+FRAME_WIDTH], start=frame):
			if card.due_as_of(args.review_date):
				ansi.bold()
				ansi.blue()
			if card.deleted:
				ansi.crossout()
				ansi.red()
			if i==sel:
				ansi.highlight()
			print(card)
			ansi.reset()
		ansi.line_wrap_on()

	def redraw_browser(frame):
		ansi.up_line(min(n, 11))
		ansi.clear_to_end()
		draw_browser(frame)
		
	frame = 0
	draw_browser(0)
	while True:

		k = 'R' if reviewing else readchar.readchar()

		sel += k=='j' and sel < len(cards)-1
		sel -= k=='k' and sel > 0


		if k in QUIT_KEYS:
				quit()
		if k in CMD_DICT:
			ansi.show_cursor()
			args.card = cards[sel] if k in ('x','s','r','R','e','E', 't') else None
			CMD_DICT[k](args)
			ansi.hide_cursor()
			reviewing = (k == 'R' and cards[sel].last_grade != 'exit')
			if reviewing and sel == n - 1:
				quit()
			elif reviewing and sel < n - 1:
				sel += 1 
		if k in GENERATORS_DICT:
			ansi.show_cursor()
			args.generator = GENERATORS_DICT[k]
			new_cards = generate(args)
			cards[sel:sel] = new_cards
			n = len(cards)
			if n < FRAME_WIDTH:
				ansi.down_line(len(new_cards))  # TODO better soln
			ansi.hide_cursor()

		frame += (frame + FRAME_WIDTH == sel)  # scroll down if we are off the screen
		frame -= (frame - 1 == sel) # scroll up if we are off the screen
		if k not in ('s','S'):
			redraw_browser(frame)
			

@subcommand(arg('pattern',nargs='?',default=''),
	arg('-v','--invert',action='store_true'),
	arg('-i','--id_only',action='store_true'),
	arg('--cards',nargs='*',type=card_type, default=ALL_CARDS),
	arg('--tags_include',nargs='*', metavar='TAGS', default=[]),
	arg('--tags_exclude',nargs='*', metavar='TAGS', default=[]),
	arg('--create_date_min',type=date_type, metavar='DATE'),
	arg('--create_date_max',type=date_type, metavar='DATE'),
	arg('--seen_date_min',type=date_type, metavar='DATE'),
	arg('--seen_date_max',type=date_type, metavar='DATE'),
	arg('--due_date_min',type=date_type, metavar='DATE'),
	arg('--due_date_max',type=date_type, metavar='DATE'),
	arg('--due_only',action='store_true'),
	arg('--not_due_only',action='store_true'),
	arg('--editor', type=str),
	arg('--reviewer', type=str),
	arg('--scheduler', type=str),
	arg('--deleted_only',action='store_true'),
	arg('--show_deleted',action='store_true'),
	arg('--new_only',action='store_true'),
	arg('--not_new_only',action='store_true'),
	alias='f', name='filter')
def display_filter(args):
	''' Filter a set of cards using a variety of parameters.
	It is often helpful to pipe this command to another one.'''

	# get filter parameters as a list of strings
	filter_kwargs = inspect.getfullargspec(filter.filter).args[1:]
	# check that args specifies these parameters
	assert all([hasattr(args, param) for param in filter_kwargs])
	matches = filter.filter(args.cards,
		# feed the keyword args editor=args.editor, due=args.due, 
		**{param : getattr(args, param) for param in filter_kwargs})
	if PIPE_OUT:
		print(*[card.id for card in matches], sep='\n', end='')
		exit()
	if len(matches) > 10:
		ansi.light()
		print(f'10 of {len(matches)}')
	ansi.line_wrap_off()
	for card in matches[:10]:
		if card.due_as_of(TODAY):
			ansi.bold(); ansi.blue()
		if card.deleted:
			ansi.crossout(); ansi.red()
		print(card.id, card, sep='\t')
		ansi.reset()
	
@subcommand()
def purge(args):
	''' Permanently delete all cards marked for deletion. '''
	deleted_cards = filter.filter(ALL_CARDS, deleted_only=True)
	if not deleted_cards:
		print('no cards are marked for deletion.')
		return
	print(f'delete {len(deleted_cards)} cards? (y/n)')
	if (confirmation := readchar.readchar()) == 'y':
		for card in deleted_cards:
			rmtree(card.path)

@subcommand(arg('backup_path',type=Path), CARDS, name='export')
def exp(args):
	for card in args.cards:
		copytree(card.path, args.backup_path / str(card.id))

@subcommand(arg('import_path',type=Path), arg('-o','--overwrite', action='store_true'), name='import')
def imp(args):
	if args.overwrite:
		rmtree(cards_path)
		copytree(args.import_path, cards_path)
		return
	old_ids = [card.id for card in ALL_CARDS]
	for new_id,card_path in enumerate(args.import_path.iterdir(), max(old_ids, default=1) + 1):
		copytree(card_path, cards_path / str(new_id))


for alias, generator in GENERATORS_DICT.items():
	p = subparsers.add_parser(generator, aliases=[alias], help='')
	p.add_argument('-t','--default_tags',nargs='*',default=[])
	p.set_defaults(func = generate, generator = generator)

# parse the command line arguments
parser.set_defaults(cards = [], func = lambda args: parser.print_help(), review_date = TODAY, scrollback = False, card = None)
# simplifiy the help message
parser._action_groups[0].title = 'commands'
parser._action_groups.pop()
args = parser.parse_args()
# accept a file of newline separated card ids
if PIPE_IN:
	ids = [int(line.strip().split()[0]) for line in sys.stdin]
	args.cards = [Card(id) for id in ids]
	sys.stdin = open('/dev/tty')  
args.func(args)

"""

--calendar
--entry
--error
--file-selection
--info
--list
--notification
--progress
--question
--text-info
--warning
--scale
--color-selection
--password
--forms

"""
import logging, subprocess
from subprocess import CalledProcessError
from pprint import pprint

TR = {ord("_"): ord("-")}

class _Command:

	title 		= None
	window_icon = None
	icon_name 	= None
	width 		= None
	height 		= None
	timeout 	= None

	def show(self):
		with subprocess.Popen(['zenity'] + self._args(),
			stdout=subprocess.PIPE,
			stderr=subprocess.STDOUT
		) as p:
			stdout,stderr = p.communicate()
			if p.returncode != 0:
				print('Error', p.returncode, p.args)
			return stdout

	def _args(self):
		keys = filter(lambda k: not k.startswith('_'), self.__dict__.keys())
		args = ["--" + type(self).__name__.lower().translate(TR)]
		for k in keys:
			args.append("--" + k.translate(TR))
			args.append(str(self.__dict__[k]))
		return args


class _TextCommand(_Command):

	text 		= None
	no_wrap 	= None
	no_markup 	= None


class Calendar(_Command):

	text 		= None
	day			= None
	month		= None
	year		= None
	date_format	= None


class Entry(_Command):

	text		= None
	entry_text	= None
	hide_text	= None


class Error(_TextCommand):
	pass


class File_Selection(_Command):

	filename			= None
	multiple			= None
	directory			= None
	save				= None
	separator			= None
	confirm_overwrite	= None
	file_filter			= None


class Info(_TextCommand):
	pass


class List(_Command):

	text			= None
	column			= None
	checklist		= None
	radiolist		= None
	separator		= None
	multiple		= None
	editable		= None
	print_column	= None
	hide_column		= None
	hide_header		= None


class Notification(_Command):

	text		= None
	listen		= None


class Progress(_Command):

	text		= None
	percentage	= None
	auto_close	= None
	auto_kill	= None
	pulsate		= None
	no_cancel	= None


class Question(_TextCommand):

	ok_label		= None
	cancel_label	= None


class Text_Info(_Command):

	filename		= None
	editable		= None
	checkbox		= None
	ok_label		= None
	cancel_label	= None


class Warning(_TextCommand):
	pass


class Scale(_Command):

	text			= None
	value			= None
	min_value		= None
	max_value		= None
	step			= None
	print_partial	= None
	hide_value		= None


class Color_Selection(_Command):

	color			= None
	show_palette	= None


class Password(_Command):

	username	= None


class Forms(_Command):

	add_entry			= None
	add_password		= None
	add_calendar		= None
	text				= None
	separator			= None
	forms_date_format	= None



if __name__ == '__main__':
	import argparse, sys, os

	p = argparse.ArgumentParser()
	p.epilog = """
	Wrapper for zenity dialogs. Usage at the command line is just for testing.
	"""

	p.add_argument("--calendar", "-d", action="store_true")
	p.add_argument("--entry", "-e", action="store_true")
	p.add_argument("--error", "-r", action="store_true")
	p.add_argument("--file-selection", "-f", action="store_true")
	p.add_argument("--info", "-i", action="store_true")
	p.add_argument("--list", "-l", action="store_true")
	p.add_argument("--notification", "-n", action="store_true")
	p.add_argument("--progress", "-p", action="store_true")
	p.add_argument("--question", "-q", action="store_true")
	p.add_argument("--text-info", "-t", action="store_true")
	p.add_argument("--warning", "-w", action="store_true")
	p.add_argument("--scale", "-s", action="store_true")
	p.add_argument("--color-selection", "-c", action="store_true")
	p.add_argument("--password", "-P", action="store_true")
	p.add_argument("--forms", "-F", action="store_true")

	p.add_argument("--verbose", "-v", action="store_true")
	options = p.parse_args()
	logging.basicConfig(
		stream=sys.stdout,
		level=logging.DEBUG if options.verbose else logging.ERROR,
		format="[%(filename)24s:%(lineno)3d] %(message)s"
	)

	if options.calendar:
		c = Calendar()
	elif options.entry:
		c = Entry()
		c.text = type(c).__name__ + " dialog"
	elif options.error:
		c = Error()
		c.text = type(c).__name__ + " dialog"
	elif options.file_selection:
		c = File_Selection()
	elif options.info:
		c = Info()
		c.text = type(c).__name__ + " dialog"
	elif options.list:
		c = List()
	elif options.notification:
		c = Notification()
		c.text = type(c).__name__ + " dialog"
	elif options.progress:
		c = Progress()
	elif options.question:
		c = Question()
		c.text = type(c).__name__ + " dialog"
	elif options.text_info:
		c = Text_Info()
		c.filename = os.path.join(os.path.dirname(__file__), 'man-zenity.txt')
		c.width = 600
		c.height = 800
	elif options.warning:
		c = Warning()
	elif options.scale:
		c = Scale()
	elif options.color_selection:
		c = Color_Selection()
		c.show_palette = True
	elif options.password:
		c = Password()
	elif options.forms:
		c = Forms()
	else:
		c = Info()
		c.text = type(c).__name__ + " dialog"

	c.title = type(c).__name__
	pprint(c.show())

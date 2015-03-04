import sublime, sublime_plugin
import os
import random
import threading

from datetime import datetime, time

timer_update = None

SUBLIME_PREFERENCES = 'Preferences.sublime-settings'

variate = False

SECONDS_PER_DAY = 60.0 * 60.0 * 24.0

def get_elapsed_seconds():
	"""
	Gets the total number of elapsed seconds in the day.
	"""
	utcnow = datetime.utcnow()
	midnight_utc = datetime.combine(utcnow.date(), time(0))
	delta = utcnow - midnight_utc
	return delta.total_seconds()

elapsed_seconds_simulated = 0.0

def get_elapsed_seconds_simulated():
	global elapsed_seconds_simulated
	elapsed_seconds_simulated = elapsed_seconds_simulated + 100.0
	if elapsed_seconds_simulated > (SECONDS_PER_DAY / 2.0):
		elapsed_seconds_simulated = 0.0
	return elapsed_seconds_simulated

class StartVariateCommand(sublime_plugin.WindowCommand):

	def run(self):
		print('started variating')

		global variate
		variate = True
		self.update()

	def update(self):

		if not variate:
			print('finished variating')
			return

		global timer_update

		sublime.load_settings(SUBLIME_PREFERENCES).set('color_scheme', 'Packages/Variate/Variate.tmTheme')

		settings_path = os.path.abspath( sublime.packages_path() + '/../' + self.window.active_view().settings().get( 'color_scheme' ) )

		from xml.dom import minidom
		xmldoc = minidom.parse(settings_path)
		itemlist = xmldoc.getElementsByTagName('dict') 

		for s in itemlist:
			if s.childNodes[1].firstChild.nodeValue == 'background':
				s.childNodes[3].firstChild.replaceWholeText(self.get_colour_time_based())

		file_handle = open(settings_path, 'wb')
		file_handle.write(bytes(xmldoc.toxml(),'UTF-8'))
		file_handle.close()

		if timer_update is not None:
			timer_update.cancel()
		timer_update = threading.Timer(1, self.update)
		timer_update.start()

	def get_colour_random(self):
		r = lambda: random.randint(0,255)
		return self.get_hex_from_rgb(int(r() * 0.5), 0, 0);

	def get_colour_time_based(self):
		"""
		Gets a colour based on the time of the day.
		"""
		return self.get_hex_from_rgb(0, 0, int(255.0 * (get_elapsed_seconds_simulated() / SECONDS_PER_DAY)))

	def get_hex_from_rgb(self, r, g, b):
		return '#%02X%02X%02X' % (r,g,b)


class StopVariateCommand(sublime_plugin.WindowCommand):

	def run(self):
		global variate
		variate = False

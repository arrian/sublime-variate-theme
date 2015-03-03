import sublime, sublime_plugin
import os
import random
import time, threading

timer_update = None

SUBLIME_PREFERENCES = 'Preferences.sublime-settings'

variate = False

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
				s.childNodes[3].firstChild.replaceWholeText(self.randomColour())

		file_handle = open(settings_path, 'wb')
		file_handle.write(bytes(xmldoc.toxml(),'UTF-8'))
		file_handle.close()

		if timer_update is not None:
			timer_update.cancel()
		timer_update = threading.Timer(1, self.update)
		timer_update.start()

	def randomColour(self):
		r = lambda: random.randint(0,255)
		return '#%02X%02X%02X' % (int(r() * 0.5),0,0)

class StopVariateCommand(sublime_plugin.WindowCommand):

	def run(self):
		global variate
		variate = False

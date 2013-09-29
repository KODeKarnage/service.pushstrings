# declare file encoding
# -*- coding: utf-8 -*-

#  Copyright (C) 2013 KodeKarnage
#
#  This Program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2, or (at your option)
#  any later version.
#
#  This Program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with XBMC; see the file COPYING.  If not, write to
#  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
#  http://www.gnu.org/copyleft/gpl.html

import sys
import xbmc
import xbmcgui
import xbmcaddon
global file_location
global auto_close

_addon_ = xbmcaddon.Addon("service.pushstrings")	
_setting_ = _addon_.getSetting
file_location = _setting_('file_location')
auto_close = _setting_('auto_close')

#import sys
#sys.stdout = open('C:\\Temp\\test.txt', 'w')

if sys.version_info >=  (2, 7):
	import json
else:
	import simplejson as json

def json_query(query):
	xbmc_request = json.dumps(query)
	result = xbmc.executeJSONRPC(xbmc_request)
	result = unicode(result, 'utf-8', errors='ignore')
	return json.loads(result)

class keyboard_monitor:

	def __init__(self):
		self._daemon()

	def push_string(self, count):
		#select_window = kbm_window("DialogSelect.xml", scriptPath, 'Default')
		#select_window.doModal()
		#del select_window
		if self.count == 0:
			self.string1 = self.process_file()
			if self.string1 != "":
				if auto_close == "true":
					self.ac = True
				else:
					self.ac = False
				self.req = json.dumps({"id": "0", "jsonrpc":"2.0", "method":"Input.SendText", "params":{"text":self.string1, "done":self.ac}})
				xbmc.executeJSONRPC(self.req)
				self.count=+1

	def process_file(self):
		if file_location != "None_Selected":
			with open(file_location,'r') as f:
				output = f.readline()	
		else:
			output = ""		
		return output

	def _daemon(self):
		#this will run constantly
		while (not xbmc.abortRequested):
			xbmc.sleep(500)
			self.count = 0
			while xbmc.getCondVisibility('Window.IsActive(virtualkeyboard)'):
				self.push_string(self.count)

	


if (__name__ == "__main__"):
	temp = keyboard_monitor()




'''
class kbm_window(xbmcgui.WindowXMLDialog):

	def onInit(self):

		self.ok = self.getControl(SAVE)
		self.ok.setLabel('Save')

		self.string_list = self.process_file()

		self.list = self.getControl(3)
		for s in self.string_list:
			tmp = xbmcgui.ListItem(str(s))
			self.list.addItem(tmp)

	def onAction(self, action):
		buttonCode = action.getButtonCode()
		actionID = action.getId()
		if (actionID in (ACTION_PREVIOUS_MENU, ACTION_NAV_BACK)):
			self.close()

	def onClick(self, controlID):
		if controlID == SAVE:
			self.close()
		else:
			selItem = self.list.getSelectedItem()

	def process_file(self):
		with open(file_location,'r') as f:
			output = f.readlines()		
		return output



ACTION_PREVIOUS_MENU = 10
ACTION_NAV_BACK = 92
SAVE = 5


'''


	

	#this should be TRUE when the keyboard is active
	#have it call a CLASS which will:
	# grab the text file,
	# read it,
	# parse it,
	# close it,
	# launch a select.xml,
	# populate with the text fields
	# on selection it will
		# close the select.xml
			# special:
				# refresh file
				# exit back to the dialog (1st choice)

		# send the text to the input field
		# click OK on the virtual keyboard
	# deletes the CLASS

# or maybe have the class created and active permanently and then have methods called from it
# while abort not requested 

	### NOTE add option to LazyTV: choose at launch
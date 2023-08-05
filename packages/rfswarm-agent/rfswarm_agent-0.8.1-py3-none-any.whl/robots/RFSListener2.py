import os
import tempfile

import sys
import socket
from datetime import datetime
import time
import requests

class RFSListener2:
	ROBOT_LISTENER_API_VERSION = 2

	msg = None
	swarmserver = "http://localhost:8138/"
	excludelibraries = ["BuiltIn","String","OperatingSystem","perftest"]

	index = 0
	vuser = 0
	iter = 0
	seq = 0

	def __init__(self):
		# print("sys.argv:",sys.argv)
		pass

	def start_suite(self, name, attrs):
		# print("metadata:", attrs['metadata'])
		# self.logmsg("metadata: {}".format(attrs['metadata']))

		if "index" in attrs['metadata']:
			self.index = attrs['metadata']["index"]

		if "iteration" in attrs['metadata']:
			self.iter = attrs['metadata']["iteration"]

		if "vuser" in attrs['metadata']:
			self.vuser = attrs['metadata']["vuser"]


	def log_message(self, message):
		# self.logmsg("message: {}".format(message))
		self.msg = message

	def end_keyword(self, name, attrs):

		if self.msg is not None:

			# message: {'timestamp': '20191208 12:27:09.175', 'message': "Opening url 'https://opencart3/'", 'level': 'INFO', 'html': 'no'}
			# name: SeleniumLibrary.Go To
			# attrs: {'kwname': 'Go To', 'libname': 'SeleniumLibrary', 'doc': 'Navigates the active browser instance to the provided ``url``.', 'args': ['${STORE URL}'], 'assign': [], 'tags': [], 'starttime': '20191208 12:27:09.175', 'endtime': '20191208 12:27:09.996', 'elapsedtime': 821, 'status': 'PASS', 'type': 'Keyword'}

			# self.logmsg("message: {}".format(self.msg))
			# self.logmsg("name: {}".format(name))
			# self.logmsg("attrs: {}".format(attrs))

			if attrs['libname'] not in self.excludelibraries:

				self.logmsg("message: {}".format(self.msg))
				self.logmsg("name: {}".format(name))
				self.logmsg("attrs: {}".format(attrs))

				self.seq += 1
				self.logmsg("{} [{}] {}".format(self.msg['message'], attrs['elapsedtime'], attrs['status']))

				startdate = datetime.strptime(attrs['starttime'], '%Y%m%d %H:%M:%S.%f')
				enddate = datetime.strptime(attrs['endtime'], '%Y%m%d %H:%M:%S.%f')

				payload = {
					"AgentName": socket.gethostname(),
					"ResultName": self.msg['message'],
					"Result": attrs['status'],
					"ElapsedTime": (attrs['elapsedtime']/1000),
					"StartTime": startdate.timestamp(),
					"EndTime": enddate.timestamp(),
					"ScriptIndex": self.index,
					"VUser": self.vuser,
					"Iteration": self.iter,
					"Sequence": self.seq
				}

				self.send_result(payload)

		self.msg = None



	def logmsg(self, msg):
		filename='./rfs_listen.txt'
		outpath = os.path.abspath(filename)
		self.outfile = open(outpath, 'a+')
		self.outfile.write("{}\n".format(msg))
		self.outfile.close()

	def send_result(self, payload):

		# Send result to server
		uri = self.swarmserver + "Result"
		# print("run_proces_output: uri", uri)

		# requiredfields = ["AgentName", "ResultName", "Result", "ElapsedTime", "StartTime", "EndTime"]

		# payload = {
		# 	"AgentName": socket.gethostname(),
		# 	"ResultName": txn,
		# 	"Result": status,
		# 	"ElapsedTime": elapsedtime,
		# 	"StartTime": startdate.timestamp(),
		# 	"EndTime": enddate.timestamp(),
		# 	"ScriptIndex": index,
		# 	"VUser": vuser,
		# 	"Iteration": iter,
		# 	"Sequence": seq
		# }

		# print("run_proces_output: payload", payload)
		try:
			r = requests.post(uri, json=payload)
			# print("run_proces_output: ",r.status_code, r.text)
			if (r.status_code != requests.codes.ok):
				self.isconnected = False
		except Exception as e:
			# print("run_proces_output: ",r.status_code, r.text)
			# print("run_proces_output: Exception: ", e)
			pass
			# print("Server Disconected", datetime.now().isoformat(sep=' ',timespec='seconds'), "(",int(time.time()),")")
			# self.isconnected = False

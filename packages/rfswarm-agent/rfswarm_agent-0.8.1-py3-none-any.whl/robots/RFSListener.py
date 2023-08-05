import os.path
import tempfile


class RFSListener:
	ROBOT_LISTENER_API_VERSION = 3

	def end_test(self, data, test):
		# self.logmsg("data: {}	{}".format(data))
		self.logmsg("test: {} [{}] {}: {}	{}".format(test, test.status, test.elapsedtime, test.doc, test.keywords))

	def logmsg(self, msg):
		filename='./rfs_listen.txt'
		outpath = os.path.abspath(filename)
		self.outfile = open(outpath, 'a+')
		self.outfile.write("{}\n".format(msg))
		self.outfile.close()

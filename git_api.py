#!/usr/bin/env python

__author__ = "aleksei.kornev@gmail.com (Aleksei Kornev)"

import config
import subprocess
import sys

from logger import get_logger 

LOGGER = get_logger("git_api")

class GitEngine: 

	def __init__(self, repo = config.repo_dir):
		self.__repo = repo

	def __exec(self, command):
		LOGGER.debug("Exec command %s" % command)
		proc = subprocess.Popen(command, cwd = self.__repo, \
					 stderr = subprocess.PIPE, \
	                                 stdout = subprocess.PIPE, \
					 shell = True)
		try:
			stdout_value = proc.stdout.read().rstrip()
			stderr_value = proc.stderr.read().rstrip()
			status = proc.wait()
		finally:
			proc.stdout.close()
			proc.stderr.close()

		LOGGER.debug("FAIL STATUS %s" % status)
		if status != 0:
			LOGGER.error("Command: %s status: %s err: %s out: %s" % (command, status, \
					stderr_value, stdout_value))
			raise GitEngineError(status, stderr_value)		

		return stdout_value	

	def fetch(self, remote_path, refs_name):
		command = "git fetch " + remote_path
		# add refs definition
		command += " +refs/heads/*:refs/remotes/%s/*" % refs_name
		
		self.__exec(command)

	def checkout(self, sha, branch_name = None):
		command = "git checkout"
		
		if branch_name is not None:
			command += " -b " + branch_name

		command += " " + sha

		self.__exec(command)
			
class GitEngineError(Exception):
	
	def __init__(self, status, error):
		self.status = status
		self.error = error

	def __str__(self):
		return repr(self.status + " " + self.error)

#if __name__ == "__main__":
#	engine = GitEngine()
#	engine.reset("HEAD^")
#	print engine.search("1")
#	engine.checkout(engine.search("h")[1], "test1")
#	engine.checkout("test/master", "test3000")
#	engine.cherry_pick("test1")
#	engine.fetch("git://github.com/teamurko/Cube.git", "cube")

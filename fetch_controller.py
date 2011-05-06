#!/usr/bin/env python

__author__ = "aleksei.kornev@gmail.com (Aleksei Kornev)"

import config
import web
import os
import fnmatch

urls = ("/sha/(\w+)", "FetchController")

class FetchController:
	
	def GET(self, sha):
		log = self.__load_log(sha)

		if not log is None:
			web.header("Content-Type", "application/octet-stream")
			web.header("Content-disposition", "attachment; "+
					"filename=%s" % log[0])
			return log[1]

		return "Error: File not found"

	def __find_file(self, path = config.repo_dir):
		for f in os.listdir(path):
			if fnmatch.fnmatch(f, config.file_pattern):
				return f
		return None
	
	def __load_log(self, sha):
		git = GitEngine()
		git.fetch(origin, "origin")
		git.checkout(sha)
		file_name = self.__find_file()

		if not file_name is None:
			log_file = open(file_name, "rb")
			return (file_name, log_file.read())

		return None

if __name__ == "__main__":
	app = web.application(urls, globals())
	app.internalerror = web.debugerror
	app.run()

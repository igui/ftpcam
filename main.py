#!/usr/bin/env python

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

from os import getenv
from sys import stderr

def main():
	ftp_user = getenv('FTP_USER')
	if not ftp_user:
		print('Must set FTP_USER env veriable', file=stderr)
		return 1

	ftp_password = getenv('FTP_PASSWORD')
	if not ftp_password:
		print('Must set FTP_PASSWORD env veriable', file=stderr)
		return 1

	authorizer = DummyAuthorizer()
	authorizer.add_user(ftp_user, ftp_password, "files", perm="ewlr")

	handler = FTPHandler
	handler.authorizer = authorizer

	server = FTPServer(("0.0.0.0", 2121), handler)
	server.serve_forever()
	return 0

if __name__ == '__main__':
	exit(main())
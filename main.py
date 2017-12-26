#!/usr/bin/env python

from types import SimpleNamespace
import logging
from os import getenv
from sys import stderr
import types

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

PASSIVE_PORTS=range(30000,30512)
FTP_PORT=2121

env_confmap = {
	'ftp_user': 'FTP_USER',
	'ftp_password': 'FTP_PASSWORD',
}

def load_configuration():
	conf = SimpleNamespace() 
	for attr, envvar in env_confmap.items():
		attr_value = getenv(envvar)
		if not attr_value:
			raise ValueError('Must set {} env veriable'.format(envvar))
		setattr(conf, attr, attr_value)
	return conf

def mantain_files

def main():
	logging.basicConfig(level=logging.DEBUG)
	
	try:
		conf = load_configuration()
	except ValueError as err:
		print(err, file=stderr)
		return 1

	authorizer = DummyAuthorizer()
	authorizer.add_user(conf.ftp_user, conf.ftp_password, "files", perm="elrw")

	handler = FTPHandler
	handler.passive_ports = PASSIVE_PORTS
	handler.authorizer = authorizer

	server = FTPServer(("0.0.0.0", FTP_PORT), handler)
	server.serve_forever()
	return 0

if __name__ == '__main__':
	exit(main())
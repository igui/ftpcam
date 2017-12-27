#!/usr/bin/env python
"""Simple FTP Server for uploading files"""

from collections import OrderedDict
from types import SimpleNamespace
from threading import Thread
import logging
import os
from sys import stderr
from stat import S_ISREG

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

MAX_DIRSIZE = 40000 # 40MB dir size
PASSIVE_PORTS = range(30000, 30020+1)
FTP_PORT = 2121
FILES_DIR = 'files'
ENV_CONFMAP = OrderedDict((
    ('ftp_user', 'FTP_USER'),
    ('ftp_password', 'FTP_PASSWORD'),
))


class CleanDirFTPHandler(FTPHandler):
    def on_file_received(self, file):
        cleardir_thread = Thread(target=self.cleardir, name="Cleardir")
        cleardir_thread.start()

    @classmethod
    def sorted_dir(cls, folder):
        """Sorts a directory in order of descending modification time"""
        def _mapstat(name):
            path = os.path.join(folder, name)
            return (path, os.stat(path))

        def _getmtime(path_stat):
            return path_stat[1].st_mtime

        def _isregular(path_stat):
            return S_ISREG(path_stat[1].st_mode)

        return sorted(
            filter(_isregular, map(_mapstat, os.listdir(folder))),
            key=_getmtime,
            reverse=True
        )

    @classmethod
    def cleardir(cls):
        """Mantains the directory as clean as possible"""
        logging.info('Processing started')
        path_stat = cls.sorted_dir(FILES_DIR)
        total_size = 0
        for path, stat in path_stat:
            total_size += stat.st_size
            if (total_size / 1024) > MAX_DIRSIZE:
                logging.info("Removing %s", path)
                try:
                    os.unlink(path)
                except OSError as ex:
                    logging.error("Couldn't remove file %s: %s", path, ex)

def load_configuration():
    """Load and check conf from environment"""
    conf = SimpleNamespace()
    for attr, envvar in ENV_CONFMAP.items():
        attr_value = os.getenv(envvar)
        if not attr_value:
            raise ValueError('Must set {} env veriable'.format(envvar))
        setattr(conf, attr, attr_value)
    return conf

def main():
    """Entry point"""
    logging.basicConfig(level=logging.DEBUG)
    try:
        conf = load_configuration()
    except ValueError as err:
        print(err, file=stderr)
        return 1

    authorizer = DummyAuthorizer()
    authorizer.add_user(conf.ftp_user, conf.ftp_password, "files", perm="elrw")

    handler = CleanDirFTPHandler
    handler.passive_ports = PASSIVE_PORTS
    handler.authorizer = authorizer

    server = FTPServer(("0.0.0.0", FTP_PORT), handler)
    server.serve_forever()
    return 0

if __name__ == '__main__':
    exit(main())

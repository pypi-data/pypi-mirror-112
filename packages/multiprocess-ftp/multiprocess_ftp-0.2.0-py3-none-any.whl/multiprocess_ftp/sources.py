import ftplib

import ftputil
import pysftp


class FTPSession(ftplib.FTP):
    """Act like ftplib.FTP constructor but connect to another port."""

    def __init__(self, host, user, passwd, port):
        """Initialize the session."""
        ftplib.FTP.__init__(self)
        self.connect(host, port)
        self.login(user, passwd)


class Connection:
    """Generic source connection."""

    def __init__(self, *args, **kwargs):
        """Setup connection details."""
        self.args = args
        self.kwargs = kwargs
        self._connection = None

    def __enter__(self):
        """Establish the connection."""
        self._connection = open(*self.args)
        return self._connection

    def __exit__(self, *args):
        """Close the connection."""
        self._connection.close()


class FTPConnection(Connection):
    """FTP session as context manager."""

    def __enter__(self):
        """Establish the connection."""
        self._connection = ftputil.FTPHost(**self.kwargs, session_factory=FTPSession)
        return self._connection


class SFTPConnection(Connection):
    """SFTP session as context manager."""

    def __enter__(self):
        self._connection = pysftp.Connection(**self.kwargs)
        return self._connection

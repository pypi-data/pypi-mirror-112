"""
TODO
"""

import os

from . import JobBase
from ..utils import fs

import logging  # isort:skip
_log = logging.getLogger(__name__)


class AutolinkJob(JobBase):
    """TODO"""

    name = 'autolink'
    label = 'Autolink'

    def initialize(self, *, torrent_filepath, locations):
        """
        Set internal state

        :param torrent_filepath: Path to torrent file
        :param locations: Sequence of directory paths that may contain files in
            `torrent_filepath`
        """
        self._torrent_filepath = str(torrent_filepath)
        self._locations = tuple(str(location) for location in locations)

    def execute(self):
        files = self._get_files_from_torrent(self._torrent_filepath)
        _log.debug('Looking for files:')
        for file in files:
            _log.debug('  %s %d', file, file.size)

        self.finish()

    def _find_filepath_by_size(self):
        for filepath in self._each_file(*self._locations):
            for file in files:
                if file.size == fs.file_size(filepath):
                    _log.debug('Found a match: %r: %r', file, filepath)
                    return filepath

    @staticmethod
    def _each_file(*locations):
        for location in locations:
            for root, dirnames, filenames in os.walk(location, followlinks=True):
                for filename in filenames:
                    yield os.path.join(root, filename)

    @staticmethod
    def _get_files_from_torrent(torrent_filepath):
        import torf
        try:
            return sorted(torf.Torrent.read(torrent_filepath).files)
        except torf.TorfError as e:
            self.error(e)

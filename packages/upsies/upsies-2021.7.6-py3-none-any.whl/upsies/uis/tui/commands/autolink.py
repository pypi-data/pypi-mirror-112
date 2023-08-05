"""
TODO
"""

from .... import defaults, errors, jobs, utils
from .base import CommandBase


class autolink(CommandBase):
    """
    TODO
    """

    names = ('autolink',)

    argument_definitions = {
        'TORRENT': {
            'help': 'Path to torrent file',
        },
        'LOCATION': {
            'nargs': '+',
            'help': 'Potential path of existing files in TORRENT',
        },
    }

    @utils.cached_property
    def jobs(self):
        return (
            jobs.autolink.AutolinkJob(
                home_directory=self.home_directory,
                cache_directory=self.cache_directory,
                torrent_filepath=self.args.TORRENT,
                locations=self.args.LOCATION,
            ),
        )

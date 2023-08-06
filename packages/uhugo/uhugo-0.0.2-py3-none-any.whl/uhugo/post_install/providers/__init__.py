from pathlib import Path
from typing import Text


class ProviderBase:
    """
    This is a base class for all the providers
    """

    def update_api(self, key: Text):
        """
        Updates an API
        :return:
        """
        pass

    def update_file(self, path: Path):
        """
        Updates a configuration file

        :param path: Path to a configuration file
        :return:
        """
        pass

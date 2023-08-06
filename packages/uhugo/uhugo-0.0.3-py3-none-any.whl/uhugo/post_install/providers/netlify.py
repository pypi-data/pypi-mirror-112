from pathlib import Path

from . import ProviderBase


class Netlify(ProviderBase):
    """
    Netlify provider
    """

    def update_file(self, path: Path):
        """
        Updates ``netlify.yaml`` file with Hugo's version

        :param path: Path of ``netlify.yaml``
        :return:
        """
        pass

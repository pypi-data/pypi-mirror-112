from pathlib import Path
from typing import Text

from uhugo.post_install.providers import ProviderBase


class Vercel(ProviderBase):
    """
    Vercel provider
    """

    def update_file(self, path: Path):
        """
        Updates ``vercel.yaml`` file with Hugo's version

        :param path: Path of ``netlify.yaml``
        :return:
        """
        pass

    def update_api(self, key: Text):
        """
        Updates Cloudflare Pages environment variable of ``HUGO_VERSION``.

        :param key: API key
        :return:
        """
        pass

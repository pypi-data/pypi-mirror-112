from typing import Text

from uhugo.post_install.providers import ProviderBase


class Cloudflare(ProviderBase):
    """
    Cloudflare provider
    """

    def update_api(self, key: Text):
        """
        Updates Cloudflare Pages environment variable of ``HUGO_VERSION``.

        :param key: API key
        :return:
        """

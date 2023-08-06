import os
from dataclasses import dataclass
from pathlib import Path
from typing import Union

# HERE = os.path.abspath(os.path.dirname(__file__))
HERE = os.getcwd()


@dataclass
class Provider:
    """
    This holds the information about the provider
    """
    name: Union[str, None]
    file_name: Union[str, None]
    key: Union[str, None]


def check_hugo_file() -> Provider:
    """
    Checks for ``config.yaml`` or ``config.toml``, if exists then it checks for ``uhugoProvider``
    and ``uhugoProviderFileName`` (this is optional)

    :return Provider: An object with ``name`` and ``file_name``
    """

    path = Path(HERE, "config.toml")
    if not path.exists():
        path = Path(HERE, "config.yaml")
        if not path.exists():
            return Provider(None, None, None)
        else:
            import yaml
            with open(path) as f:
                data = yaml.load(f)
    else:
        import toml
        with open(path) as f:
            data = toml.load(f)

    return Provider(data.get("uhugoProvider", None), data.get("uhugoProviderFileName", None), data.get("uhugoProviderKey", None))


def check_fs() -> Union[Provider, None]:
    """
    Checks file system for any providers that matches the list

    :return: A Provider
    """

    files = ["netlify.yaml", "vercel.json"]

    for file in files:
        path = Path(HERE, file)
        if path.exists():
            return Provider(path.name.split(".")[0], path.__str__(), None)

    return None

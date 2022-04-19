import os

import toml


config = toml.load("scripty/constants/config.toml")


if __name__ == "__main__":
    if os.name != "nt":
        import uvloop

        uvloop.install()

import os

from scripty import AppBot


if __name__ == "__main__":
    if os.name != "nt":
        import uvloop

        uvloop.install()

    AppBot().run()

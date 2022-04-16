import os

import scripty


if __name__ == "__main__":
    if os.name != "nt":
        import uvloop

        uvloop.install()

    scripty.core.run()

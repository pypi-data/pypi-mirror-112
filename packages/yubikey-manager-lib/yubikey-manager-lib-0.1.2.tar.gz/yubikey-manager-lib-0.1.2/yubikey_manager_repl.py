import io
import logging
import warnings
import contextlib
import json

from cryptography.utils import CryptographyDeprecationWarning

with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=CryptographyDeprecationWarning)
    import ykman.cli.__main__

# Restore logger, set by ykman.cli.__main__ import
logging.disable(logging.NOTSET)


def main():
    """
    Main function, make ykman calls without restarting the python process
    Reads input in JSON format
    Returns output in JSON output
    """
    while 1:
        line = input()
        if not line:
            break

        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr), contextlib.redirect_stdout(stdout):
            try:
                ykman.cli.__main__.cli.main(args=json.loads(line))
            except SystemExit:
                pass
        print(
            json.dumps(
                {
                    "stdout": stdout.getvalue().splitlines(),
                    "stderr": stderr.getvalue().splitlines(),
                }
            ),
            flush=True,
        )

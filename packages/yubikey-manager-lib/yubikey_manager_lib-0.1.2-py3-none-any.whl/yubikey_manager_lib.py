import subprocess
import json
import pathlib
import sys
import shutil


class YKMan:
    def __init__(self, ykman_repl="ykman-repl"):
        full_ykman_repl = shutil.which(ykman_repl)

        if not full_ykman_repl:
            p = pathlib.Path(sys.argv[0])
            full_ykman_repl = p.parent / "ykman-repl"
            if not full_ykman_repl.exists():
                full_ykman_repl = None

        self._ykman = subprocess.Popen(
            [full_ykman_repl],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            universal_newlines=True,
            bufsize=1,
        )

    def run(self, *args):
        self._ykman.stdin.write(json.dumps(args) + "\n")
        stdout = self._ykman.stdout.readline()
        return json.loads(stdout)

    def __del__(self):
        self._ykman.communicate("\n")

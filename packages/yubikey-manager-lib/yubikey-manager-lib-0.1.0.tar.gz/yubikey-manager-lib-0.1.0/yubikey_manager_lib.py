import subprocess
import json


class YKMan:
    def __init__(self):
        self._ykman = subprocess.Popen(
            ["ykman-repl"],
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

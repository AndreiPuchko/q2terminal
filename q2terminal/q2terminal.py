import sys
from subprocess import Popen, PIPE, STDOUT
from time import ctime


class Q2Terminal:
    def __init__(self, terminal=None, echo=False, callback=None):
        self.echo = False
        self.callback = None
        if terminal is None:
            if "win32" in sys.platform:
                terminal = "powershell"
            elif "darwin":
                terminal = "zsh"
            else:
                terminal = "bash"
        self.proc = Popen(
            [terminal],
            stdin=PIPE,
            stdout=PIPE,
            stderr=STDOUT,
        )
        self.run("echo 0")
        self.echo = echo
        self.callback = callback
        self.exit_code = None

    def run(self, cmd="", echo=False, callback=None):
        if echo or self.echo:
            print(f"{ctime()}> {cmd}>")
        _callback = callback if callback else self.callback
        self.exit_code = None
        cmd = f"{cmd};$?;echo q2eoc\n"
        self.proc.stdin.writelines([bytes(cmd, "utf8")])
        self.proc.stdin.flush()
        rez = []
        first_line = True
        while self.proc.poll() is None:
            line = self.proc.stdout.readline().decode("utf8").rstrip()
            if not line:
                continue
            if first_line:
                first_line = False
                continue

            if line.strip() == "q2eoc":
                if rez:
                    self.exit_code = rez.pop().strip()
                    if self.exit_code.isdigit():
                        self.exit_code = int(self.exit_code)
                    elif self.exit_code == "True":
                        self.exit_code = True
                    elif self.exit_code == "False":
                        self.exit_code = False
                break
            elif line == "":
                continue
            else:
                rez.append(line)
                if echo or self.echo:
                    print(f"{ctime()}: {line}")
                if callable(_callback):
                    callback(line)

        return rez

    def close(self):
        self.proc.terminate()

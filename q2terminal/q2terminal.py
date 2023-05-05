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
                    self.exit_code = rez.pop()
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


if __name__ == "__main__":
    q2t = Q2Terminal()

    # print(q2t.run("$q2 = 123"))
    # print(q2t.run("echo $q2"))
    # print(q2t.run("git status"))
    # print(q2t.exit_code)

    # print(q2t.run("pwd"))
    # print(q2t.run("pushd"))
    # print(q2t.run("cd \\"))
    # print(q2t.run("pwd"))
    # print(q2t.run("popd"))
    print(q2t.run("cd C:/Users/andre/Documents/penta.new.local/"))
    print(q2t.run("pwd", echo=1))

    def cb(line):
        print(line)
        if "tarting as process" in line:
            sys.exit(100)

    print(q2t.run("cmd /c penta.exe", callback=cb))
    print(q2t.run("py3 --version", echo=1))
    print(q2t.exit_code)

    q2t.close()

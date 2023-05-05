from q2terminal.q2terminal import Q2Terminal
import sys


def test_01_01():
    t = Q2Terminal()
    t.run(r"pwd", echo=True)
    assert t.exit_code is True
    print(t.run("git status"))
    assert t.exit_code is True
    assert "q2terminal.py" in " ".join(t.run("ls q2terminal/*.py"))
    t.close()


def test_01_02():
    t = Q2Terminal(echo=True)
    assert t.run("$q2 = 123") == []
    assert t.run("echo $q2") == ["123"]
    t.close()


def test_01_03():
    t = Q2Terminal()
    current_folder = t.run("pwd")[2]
    t.run("pushd")
    t.run("cd /")
    t.run("pwd", echo=1)

    t.run("pwd 1")
    assert t.exit_code is False

    t.run("popd")
    assert t.run("pwd")[2] == current_folder


def test_01_04():
    files = []

    def cb(line):
        if line[34:50].strip().isdigit():
            files.append(line[50:])

    t = Q2Terminal()
    t.run("ls", callback=cb)
    if t.exit_code is True:
        print(files)


def test_01_05():
    t = Q2Terminal()
    t.run("programm", echo=True)
    assert t.exit_code is False
    if "win32" in sys.platform:
        t.run("notepad")
        assert t.exit_code is True


if __name__ == "__main__":
    test_01_01()
    test_01_02()
    test_01_03()
    test_01_04()
    test_01_05()

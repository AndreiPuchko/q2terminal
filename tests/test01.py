if __name__ == "__main__":
    import sys

    if "." not in sys.path:
        sys.path.insert(0, ".")

from q2terminal.q2terminal import Q2Terminal


def test_01_01():
    t = Q2Terminal()
    t.run(r"pwd", echo=True)
    assert t.exit_code == "True"
    print(t.run("git status 1"))
    assert t.exit_code == "True"
    assert "q2terminal.py" in " ".join(t.run("ls q2terminal/*.py"))


if __name__ == "__main__":
    test_01_01()
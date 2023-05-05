import sys



# sys.path.append("../q2terminal")
sys.path.append("..")

from q2terminal.q2terminal.q2terminal import Q2Terminal

t = Q2Terminal()
print(t.run(r" cd C:\Users\andre\Desktop\dev\q2\q2market"))
print(t.run("git status"))

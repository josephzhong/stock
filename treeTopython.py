import re

p = re.compile("(?P<indent> *)(?P<compare>[a-zA-Z_]* (<=|>) [0-9.\-]*)"
               "(: (?P<result>[a-zA-Z]*) (?P<score>\([0-9.]*(/[0-9.]*)?\)))?\n?")
file = open("tree7y600pre.tree")
pythonFile = open("tree7y600pre.py", "w")
for line in file.readlines():
    line = line.replace("|", " ")
    m = p.match(line)
    if m is not None:
        indent = m.group("indent")
        compare = m.group("compare")
        result = m.group("result")
        score = m.group("score")
        line = "{0}if ({1}):\n".format(indent, compare)
        if result is not None and score is not None :
            line += "{0}    {1} = {2}\n".format(indent, result, score)
        pythonFile.write(line)
    else:
        print(line)
file.close()
pythonFile.close()

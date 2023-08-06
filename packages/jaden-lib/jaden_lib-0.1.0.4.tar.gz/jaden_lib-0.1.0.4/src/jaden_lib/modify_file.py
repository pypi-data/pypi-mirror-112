def modify(file, old=None, new=None, combination=None, whole=None, delete=False, read=False):
    if read is True:
        with open(file, "r", encoding="utf-8-sig") as f:
            return f.read()
    elif delete is True:
        import os
        os.remove(file)
        return
    elif whole != None:
        with open(file, "w", encoding="utf-8-sig") as f:
            if type(whole) == list:
                for i in whole:
                    f.write(i + "\n")
            elif type(whole) == str:
                f.write(whole)
        return
    fileContent = ""
    if combination != None:
        old = list(combination.keys())
        new = list(combination.values())
    elif old is None or new is None:
        raise Exception("没有old或new")
    with open(file, "r+", encoding="utf-8-sig") as f:
        c = 0
        for line in f:
            if type(new) == list:
                for i in old:
                    if i in line:
                        line = line.replace(i, new[c])
                        old.pop(c)
                        new.pop(c)
                    c += 1
            elif type(old) == str and old in line:
                line = line.replace(old, new)
            c = 0
            fileContent += line
        f.write(fileContent)
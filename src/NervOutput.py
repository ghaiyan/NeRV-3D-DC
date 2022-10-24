import fileinput
def del_firstline(delfile):
    for line in fileinput.input(delfile, inplace = 1):
        if not fileinput.isfirstline():
            print(line.replace("\n", ""))


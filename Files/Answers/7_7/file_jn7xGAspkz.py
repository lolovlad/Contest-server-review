from time import sleep

with open("input.txt") as file:
    s = file.readline().replace("\n", "")
    move_n = 0
    move_e = 0
    num = 0
    for c in s:
        if c == 'N':
            move_n += num
            num = 0
        elif c == 'S':
            move_n -= num
            num = 0
        elif c == 'E':
            move_e += num
            num = 0
        elif c == 'W':
            move_e -= num
            num = 0
        else:
            num = num * 10 + int(c)


with open("output.txt", "w") as file:
    if move_n > 0:
        file.writelines("".join([str(move_n), "N"]))
    if move_n < 0:
        file.writelines("".join([str(-move_n), "S"]))
    if move_e > 0:
        file.writelines("".join([str(move_e), "E"]))
    if move_e < 0:
        file.writelines("".join([str(-move_e), "W"]))
    file.writelines("\n")


# coding=utf-8
import os, time, json

def main():

    directory = os.path.dirname(os.path.realpath(__file__))

    def getbrd():
        f = open(directory+"/levels.txt","r")
        row2 = []
        levels = []
        for line in f:
            if line.replace('\n','')=="": 
                levels.append(row2)
                row2 = []
            else:
                row2.append(line.replace('\n',''))

        f.close()
        return levels


    levels = getbrd()
    olvl = getbrd()

    level = 1
    steps = 0

    class Player:
        def __init__(self):
            self.x = len(levels[level-1][len(levels[level-1])//2])//2
            self.y = len(levels[level-1])//2

    def getText(i):
        if i == 0:
            return " ┌────────────┐"
        elif i == 1:
            return " │ STEPS: "+str(steps)+(" "*(4-len(str(steps)))+"│")
        elif i == 2:
            return " │ LEVEL: "+str(level)+(" "*(4-len(str(level)))+"│")
        elif i == (len(levels[level-1])-1):
            return " └────────────┘"
        elif i > (len(levels[level-1])-1):
            return ""
        else:
            return " │            │"

    levels = getbrd()
    olvl = getbrd()

    level = 1
    steps = 0

    p = Player()

    while True:   

        os.system('clear') 

        h  = os.get_terminal_size()[1]
        h2 = h-(len(levels[level-1])*2)
        h3 = h2//2

        print("\n"*h3)

        w  = os.get_terminal_size()[0]
        w2 = w-(len(levels[level-1][0])*2)
        w3 = w2//2

        for i in range(len(levels[level-1])):
            row = "" 
            for j in range(len(levels[level-1][i])):
                if i==p.y and j == p.x:
                    row += ("\033[91m @\033[00m")
                else:
                    if levels[level-1][i][j] == "J": 
                        row +=" \033[92m.\033[00m"
                    elif levels[level-1][i][j] == "■": row += " \033[94m■\033[0m"
                    elif levels[level-1][i][j] == ".": row += " \033[90m.\033[0m"
                    else: row += " "+levels[level-1][i][j]

            print((" "*(w3-10))+row+getText(i))

        k = input((" "*(w3-10))+"Type WASD, R or Q: ")

        tx = p.x
        ty = p.y

        xc = 0
        yc = 0

        if k == 'r':
            p.x = len(levels[level-1][len(levels[level-1])//2])//2
            p.y = len(levels[level-1])//2
            steps = 0

            levels[level-1] = getbrd()[level-1]

        else:

            if k == "w": yc -= 1
            elif k == "s": yc += 1
            elif k == "a": xc -= 1
            elif k == "d": xc += 1
            elif k == "q": return "QUIT"

            tx += xc
            ty += yc

            if levels[level-1][ty][tx] == "." or levels[level-1][ty][tx] == "J":
                steps += 1
                p.x = tx
                p.y = ty

            elif levels[level-1][ty][tx] == "■":
                if levels[level-1][ty+yc][tx+xc] == "." or levels[level-1][ty+yc][tx+xc] == "J":
                    p.x = tx
                    p.y = ty
                    l = list(levels[level-1][ty])
                    if olvl[level-1][ty][tx]=="J": 
                        l[tx] = "J"
                    else: l[tx] = "."

                    levels[level-1][ty] = "".join(l)

                    l = list(levels[level-1][ty+yc])
                    l[tx+xc] = "■"
                    levels[level-1][ty+yc] = "".join(l)

                    steps += 1

            jc = 0

            for i in range(len(levels[level-1])):
                jc += levels[level-1][i].count("J")

            if jc == 0:
                steps = 0
                level += 1
                if level > len(levels):
                    return "WIN" 
                    level = 1
                    levels = getbrd()
                p.x = len(levels[level-1][len(levels[level-1])//2])//2
                p.y = len(levels[level-1])//2

            if level > len(levels): 
                return "WIN"

if __name__ == "__main__":
    main()
import os, random, time, land, item_data
import text_colors as tc

class Sky():
    def __init__(self):
        self.stars = []
        self.colors = [235, 237, 239, 241, 243, 245, 247, 249, 251, 253, 255]

s = Sky()

tips = [
    "This game was originally called 'RPG'",
    "There's a arcade machine hidden in the alps",
    "An alternate name for this game was 'FAR'",
    "This engine was created in two days",
    "'Look around' can be shortened to 'l'",
    "You can use 'n' instead of 'go north'",
    "This isn't actually loading, but it looks cool",
    "If you die, you reset to the nearest temple",
    "There are no inventory limits",
    "Watch out for quicksand in the desert",
    "There are five different shards to collect",
    "This game has "+str(len(land.all))+" different tiles",
    "This game has "+str(len(item_data.items))+" different items",
    "Your progress is automatically saved",
    "I'm writing these the day before my birthday",
    "This game was never meant to be a sequel",
    "418: I'm a little teapot, short and stout",
    "Snag any potions you can find",
    "You can drop items to make a trail",
    "Hopefully, a sequel doesn't take another 2 years",
    "This game was made in pure Python",
    "This game is about 2.5k lines of code",
    "This game is made by PixelDip",
    "First ever use of colors in a C&C game",
    "This game was made in about a week",
    "There are five realms in this game",
    "Graphics like this are really hard to make",
    "The code for this game is about 200 kb",
    "The original C&C only had 38 tiles",
    "The original C&C was only 38 kb",
    "Most of this game was created past midnight",
    "The credits are based off Star Trek TNG",
    "There's a shop at the end of every level",
    "Type 'help' to get help (suprise!)",
    "This game was coded entirely on a macbook"
]

credit = [
    ["CASTLES AND CHAMBERS 2",
    "                      "],
    [tc.BOLD+"FEEDBACK"+tc.ENDC,
    "                ",
    "DUNCAN HEYWOOD",
    "GENTRY UNDERWOOD",
    ""],
    [tc.BOLD+"BETA TESTING"+tc.ENDC,
    "                  ",
    "MICHELLE UNDERWOOD",
    "AUSTIN UNDERWOOD",
    "GENTRY UNDERWOOD",
    "DUNCAN HEYWOOD",
    "SETH PACARD"],
    [tc.BOLD+"CREATED BY RONAN UNDERWOOD"+tc.ENDC,
             "                         "],
    ["PixelDip STUDIOS",
     "                     "],
    ["",""],
    ["THANK YOU FOR PLAYING",
     "                     "],

]

tips.append("There are "+str(len(tips)+2)+" different tips that display here")

def windowWidth():
    return os.get_terminal_size()[0]

def windowHeight():
    return os.get_terminal_size()[1]

def createField():
    for i in range(windowHeight()):
        addrow()

def drawFrame(txt):
    os.system('clear')
    w = (windowWidth()-len(txt[1]))//2
    h = (windowHeight()-len(txt))//2
    for i in range(len(s.stars)):
        row = []
        for j in range(len(s.stars[i])):
            if i >= h and i < len(txt)+h and j >= w and j < len(txt[i-h])+w:
                row.append(txt[i-h][j-w])
            elif str(s.stars[i][j]).isnumeric():
                row.append("\033[38;5;"+str(s.colors[s.stars[i][j]])+"m.\u001b[0m")
            else:
                row.append(" ")

        print("".join(row))

def addrow():
    row = []
    for i in range(0, windowWidth()):
        row.append(" ")

    for i in range(0, (windowWidth()//20)):
        row[random.randint(0, windowWidth()-1)] = random.randint(0, len(s.colors)-1)

    s.stars.append(row)

def update():
    del s.stars[0]

    addrow()

def draw(t):

    introtext = '''
      _____         __  __                       __
     / ___/__ ____ / /_/ /__ ___   ___ ____  ___/ /
    / /__/ _ `(_-</ __/ / -_|_-<  / _ `/ _ \/ _  /
    \___/\_,_/___/\__/_/\__/___/  \_,_/_//_/\_,_/
      _______              __                 ___
     / ___/ /  ___ ___ _  / /  ___ _______   |_  |
    / /__/ _ \/ _ `/  ' \/ _ \/ -_) __(_-<  / __/
    \___/_//_/\_,_/_/_/_/_.__/\__/_/ /___/ /____/

    '''

    createField()
    intro = []
    introtext = list(introtext)
    row = ""

    for i in range(len(introtext)):
        if introtext[i] == "\n":
            intro.append(row)
            row = ""
        else:
            row += introtext[i]

    if random.randint(0, 100) == 1: z = "This message has a 1% chance of being found"
    else: z = random.choice(tips)
    b = " "*((len(intro[-2])-len(z))//2)
    intro.append(b+z+b)

    for i in range(int(t/0.3)):
        drawFrame(intro)
        update()
        time.sleep(0.3)

def draw_sect(i, t):
    for _ in range(int(float(i)/0.3)):
        drawFrame(t)
        update()
        time.sleep(0.3)

def draw_credits():
    s.stars = []
    createField()
    for i in range(len(credit)):
        draw_sect(3, credit[i])

if __name__ == "__main__":
    draw(5)
    draw_credits()
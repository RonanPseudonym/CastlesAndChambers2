# coding=utf-8

global name

import os, textwrap, re, difflib, time, random, land, player, cut_data, item_data, stars, pathlib, time
import new_sokoban as sokoban
import text_colors as tc

directory = os.path.dirname(os.path.realpath(__file__))

class Lang:
    def __init__(self):
        self.helpcmd = tc.BOLD+'''LOOK AROUND - L:'''+tc.ENDC+''' Shows you your current location\n'''+tc.BOLD+'''LOOK AT:'''+tc.ENDC+''' Look at an item\n'''+tc.BOLD+'''GO NORTH, ETC - N:'''+tc.ENDC+''' Move in said direction\n'''+tc.BOLD+'''PICK UP:'''+tc.ENDC+''' Take an item\n'''+tc.BOLD+'''DROP:'''+tc.ENDC+''' Drop an item\n'''+tc.BOLD+'''OPEN DOOR:'''+tc.ENDC+''' Opens door\n'''+tc.BOLD+'''USE:'''+tc.ENDC+''' Use an item\n'''+tc.BOLD+'''INVENTORY - INV:'''+tc.ENDC+''' Check inventory\n'''+tc.BOLD+'''QUIT: '''+tc.ENDC+'''Return to main menu\n\nYou control this game with text commands, such as 'go east' or 'take ticket'. Never say 'go to [x]', use directional commands instead.\n\nThere are all sorts of puzzles and dangers in this game, so be prepared!'''

        self.begin = [
            "go",
            "view",
            "take",
            "drop",
            "open",
            "use"
        ]

        self.autoreply = {
            "pick up small green man eating pizza": "You attempt to pick up the green man, but he runs away at an impressively swift pace. Your finger, instead, crushes the pizza, not unlike the crushing of the small green man's hopes and dreams after the war of smallpizza.", # This is not my fault. This is not my choice. I am being held hostage and forced to add this. May God redeem my soul.

            "zork": "Wrong game, but I appreciate the sentiment."
        }

        self.end = [
            "north",
            "east",
            "south",
            "west",
            "door",
        ]

        self.cutscenes = cut_data.cutscenes

        self.spesh = [
            "look",
            "inventory",
            "clear",
            "exit",
            "quit",
            "loc",
            "shop",
            "help"
        ]

        self.sub = {
            "n": "go north",
            "north": "go north",
            "e": "go east",
            "east": "go east",
            "s": "go south",
            "south": "go south",
            "w": "go west",
            "west": "go west",
            "inv": "inventory",
            "get": "take",
            "grab": "take",
            "look around": "look",
            "l": "look",
            "look at": "view",
            "pick up": "take",
            "the": "",
            "i": "",
        }

        credit = [
            "CASTLES AND CHAMBERS 2",
            "",
            tc.BOLD+"FEEDBACK"+tc.ENDC,
            "",
            "DUNCAN HEYWOOD",
            "GENTRY UNDERWOOD",
            "",
            "",
            tc.BOLD+"BETA TESTING"+tc.ENDC,
            "",
            "MICHELLE UNDERWOOD",
            "AUSTIN UNDERWOOD",
            "GENTRY UNDERWOOD",
            "DUNCAN HEYWOOD",
            "",
            "",
            tc.BOLD+"CREATED BY RONAN UNDERWOOD"+tc.ENDC,
            "",
            "",
            "PixelDip STUDIOS"
        ]

        self.escape = [
            '''\033[95m''',
            '''\033[94m''',
            '''\033[96m''',
            '''\033[92m''',
            '''\033[93m''',
            '''\033[91m''',
            '''\033[0m''',
            '''\033[1m''',
            '''\033[4m''',
        ]

        self.data = []

        self.items = item_data.items
        self.healthitems = item_data.health

    def getlocdata(self, full, x, y):
        for i in range(len(land.all)):
            if land.all[i]['x'] == x and land.all[i]['y'] == y:
                n = tc.BOLD+land.all[i]['name']+tc.ENDC

                items = ""
                for j in range(len(list(land.all[i]['items']))):
                    items += tc.OKCYAN+"\nThere is a "+land.all[i]['items'][j]+" here."+tc.ENDC

                if tuple([x, y]) in cut_data.cutcom:
                    items += tc.OKBLUE+"\nThere's a shop here. Type 'shop' to enter."+tc.ENDC

                if full or land.all[i]['gone'] == False:

                    land.all[i]['gone'] = True
                    uberdesc = land.all[i]['desc']

                    self.data.append(n+"\n"+uberdesc+items)
                else:
                    self.data.append(n+items)

    def getproperty(self, x, y):
        for i in range(len(land.all)):
            if land.all[i]['x'] == x and land.all[i]['y'] == y:
                return land.all[i]

        return "LOT_ERROR"

    def titleCase(self, t):
        xz = t
        xz = list(xz)
        xz[0] = xz[0].upper()
        xz = "".join(xz)

        return xz

    def parseInp(self, inp):
        if inp[0] == "go":
            nx = player.x
            ny = player.y
            if inp[1] == "north": ny += 1
            if inp[1] == "south": ny -= 1
            if inp[1] == "east": nx += 1
            if inp[1] == "west": nx -= 1

            possible = False

            for i in range(len(land.all)):
                if land.all[i]['x'] == nx and land.all[i]['y'] == ny:
                    possible = True
                    break

            if possible:
                a = str([[player.x, player.y],[nx, ny]])
                b = str([[nx, ny],[player.x, player.y]])

                ds = True

                if a in land.doors.keys():
                    ds = land.doors[a]['open']

                if b in land.doors.keys():
                    ds = land.doors[b]['open']

                if ds:

                    if a in land.walls or b in land.walls:
                        self.data.append(tc.FAIL+"There's a wall here."+tc.ENDC)

                    else:

                        player.oldx = player.x
                        player.oldy = player.y

                        player.x = nx
                        player.y = ny

                        if not (player.x == 100 and player.y == 108 and not 'Axe' in player.inv): self.getlocdata(False, player.x, player.y)

                else:
                    self.data.append(tc.FAIL+"The door is closed."+tc.ENDC)

            else:
                self.data.append(tc.FAIL+"You can't go any further "+inp[1]+tc.ENDC)

        elif inp[0] == "view":
            k = self.titleCase(inp[1])
            if k.lower() in list(self.items):
                if k in list(player.inv) or k.lower() in self.getproperty(player.x, player.y)['items']:
                    self.data.append(self.items[k.lower()])
                else:
                    self.data.append(tc.FAIL+"I don't see a "+inp[1]+" here..."+tc.ENDC)
            else:
                self.data.append(tc.FAIL+"You can't look at that."+tc.ENDC)

        elif inp[0] == "use":
            if self.titleCase(inp[1]) in player.inv:
                if inp[1] == "axe":
                    if "tree" in self.getproperty(player.x, player.y)['desc']:
                        if player.x == 98 and player.y == 106 and not 'Yellow shard' in player.inv:
                            self.data.append("You cut down the tree, with sizable effort. It falls in the water, with a large splash. The crystal falls out onto the ground, and you can now tell clearly that it is a yellow shard.")
                            for i in range(len(land.all)):
                                if land.all[i]['x'] == player.x and land.all[i]['y'] == player.y:
                                    land.all[i]['items'].append("yellow shard")
                                    break
                        else:
                            self.data.append(tc.FAIL+"You cut down the tree, but nothing eventful transpires. Nice job, you just cut down a tree. I hope you feel good about yourself."+tc.ENDC)
                    else:
                        self.data.append(tc.FAIL+"You don't see a tree here."+tc.ENDC)

                elif inp[1] == "pickaxe":
                    if player.x == 109 and player.y == 121:
                        if 'Pickaxe' in player.inv or 'pickaxe' in getproperty(player.x, player.y):
                            self.data.append("You start mining, chipping little bits off. It takes a while, but you're able to mine away the rock, revealing a key. You pick it up.")
                            player.inv.append("Gold key")

                        else:
                            self.data.append(tc.FAIL+"You've already used that"+tc.ENDC)
                    else:
                        self.data.append(tc.FAIL+"You can't use that here."+tc.ENDC)

                elif inp[1] == "crystal" and player.x == 203 and player.y == 203:
                    if player.won == False:
                        player.won = True

                        player.x = 1000
                        player.y = 1000

                    else:
                        self.data.append(tc.FAIL+"You already did that"+tc.ENDC)


                elif inp[1] == "sweater":
                    if not "sweater" in player.ineffect:
                        self.data.append("You put on the sweater. It's a bit scratchy, but is extremely warm.")
                        player.ineffect.append("sweater")
                    else:
                        self.data.append(tc.FAIL+"You already have the sweater on"+tc.ENDC)

                elif inp[1] in list(self.healthitems): 
                    player.health+=self.healthitems[inp[1]]
                    self.data.append("Increased health by "+str(self.healthitems[inp[1]]))
                    del player.inv[player.inv.index(self.titleCase(inp[1]))]

                else:
                    self.data.append(tc.FAIL+"You can't use a "+inp[1]+" right now"+tc.ENDC)

            else: 
                self.data.append(tc.FAIL+"You don't have a "+inp[1]+tc.ENDC)

        elif inp[0] == "open" and inp[1] == "door":
            k = list(land.doors.keys())
            for i in range(len(k)):
                if str([player.x, player.y]) in k[i]:
                    if land.doors[k[i]]['open']:
                        self.data.append(tc.FAIL+"The door is already open"+tc.ENDC)
                    else:
                        z = land.doors[k[i]]

                        if z['require'] == ".none" or self.titleCase(z['require']) in player.inv:
                            land.doors[k[i]]['open'] = True
                            if z['txt'] == ".none":
                                self.data.append("Open")
                            else:
                                if player.x == 0 and player.y == -2:
                                    if player.won == False:
                                        self.data.append("The door gobbles your ticket, and slides open. Instead of the normal train, a portal opens to your south. It pulsates, impossibly blue deep. No one else seems to notice it, walking through it and straight onto the other side.")
                                    else:
                                        self.data.append("The door gobbles your ticket, and the door slides open.")

                                else:
                                    self.data.append(z['txt'])

                            if z['use']: del player.inv[player.inv.index(self.titleCase(z['require']))]

                        else:
                            self.data.append(tc.FAIL+"You need a "+z['require']+tc.ENDC)                           

                    break

        elif inp[0] == "drop":
            k = self.titleCase(inp[1])
            if k in list(player.inv):
                del player.inv [player.inv.index(k)]
                self.data.append("You dropped the "+k.lower())

                for i in range(len(land.all)):
                    if land.all[i]['x'] == player.x and land.all[i]['y'] == player.y:
                        land.all[i]['items'].append(inp[1])
            else:
                self.data.append(tc.FAIL+"You don't have a "+inp[1]+tc.ENDC)

        elif inp[0] == "take":
            x = self.getproperty(player.x, player.y)
            xz = inp[1]
            has = False
            for i in range(len(x['items'])):
                if x['items'][i] == inp[1]:
                    del x['items'][i]
                    xz = inp[1]
                    xz = list(xz)
                    xz[0] = xz[0].upper()
                    xz = "".join(xz)

                    if xz == "Coin": player.gold += 1
                    elif xz == "Poster":
                        for j in range(len(land.all)):
                            if land.all[j]['x'] == player.x and land.all[j]['y'] == player.y:
                                self.data.append("You take the poster, and notice something fall out from behind it. It appears to be a key.")
                                player.inv.append("Poster")
                                land.all[j]['items'].append("key")


                    else: player.inv.append(xz)

                    has = True

                    break

            if has and xz != "Poster":
                self.data.append("Taken.\n"+self.items[inp[1]])
            elif xz != "Poster":
                self.data.append(tc.FAIL+"I don't see a "+inp[1]+" around here"+tc.ENDC)

    def getdir(self, xp, yp):
        z = self.getproperty(player.x+xp, player.y+yp)

        if z == "LOT_ERROR":
            return "None"+(" "*(11-len("None")))
        else:
            if str([[player.x+xp, player.y+yp], [player.x, player.y]]) in land.walls or str([[player.x, player.y], [player.x+xp, player.y+yp]]) in land.walls:
                return "Wall"+(" "*(11-len("Wall")))

            # print(list(land.doors.keys()))
            a = str([[player.x+xp, player.y+yp], [player.x, player.y]])
            b = str([[player.x, player.y], [player.x+xp, player.y+yp]])
            # exit()

            if a in list(land.doors.keys()) and land.doors[a]['open'] == False:
                return "Door"+(" "*(11-len("Door")))

            if b in list(land.doors.keys()) and land.doors[b]['open'] == False:
                return "Door"+(" "*(11-len("Door")))

            return tc.OKCYAN+z['name']+tc.ENDC+(" "*(11-len(z['name'])))

    def getChars(self, txt, c):
        txt = list(txt)
        for _ in range(len(txt)-c):
            del txt[-1]
        return "".join(txt)
    
    def drawCutscene(self):
        if (player.x, player.y) in cut_data.cutcom:
            if cut_data.cutcom.index((player.x, player.y))>=(player.level-1):

                i = player.level-1

                player.level += 1

                h = '\n'*((os.get_terminal_size()[1]-21)//2)
                buffer = " "*((os.get_terminal_size()[0]-66)//2)

                for j in range(len(self.cutscenes[i])):
                    for k in range(round(len(self.cutscenes[i][j])*1.3)):
                        time.sleep(0.05)
                        os.system('clear')
                        print(h)
                        print(self.getChars(self.cutscenes[i][j].replace('\n','@'), k).replace("@","\n"+buffer))
                        

                os.system("clear")
    def getLine(self, line, menu):
        if menu:
            if line == 0: return "┌────────────────────┐"
            if line == 1: return "│ "+tc.BOLD+"PLAYERS"+tc.ENDC+"            │"
            if line == 2: return "│                    │"
            elif line == 19: return "└────────────────────┘"
            else:
                pl = get_players()
                if line <= len(pl)+2:
                    if pl[line-3] == "None": return "│ None               │"
                    else: return "│ "+tc.OKCYAN+pl[line-3]+tc.ENDC+(" "*(19-len(pl[line-3])))+"│"
                else:            return "│                    │"

        else:
            if line == 0:    return "┌────────────────────┐"
            elif line == 18: return "│ "+tc.DARKGREY+"PixelDip"+tc.ENDC+"           │"
            elif line == 19: return "└────────────────────┘"
            elif line == 1: return "│ "+tc.BOLD+"DATA               "+tc.ENDC+"│"
            elif line == 3:  return "│ LOC:    "+self.getdir(0, 0)+"│"
            elif line == 5: return "│ "+tc.BOLD+"PROFILE            "+tc.ENDC+"│"
            elif line == 7:  return  "│ HEALTH: "+tc.FAIL+str(player.health)+tc.ENDC+(" "*(11-len(str(player.health))))+"│"
            elif line == 8:  return  "│ GOLD:   "+tc.WARNING+str(player.gold)+tc.ENDC+(" "*(11-len(str(player.gold))))+"│"
            elif line == 9:  return  "│ LEVEL:  "+tc.WARNING+str(player.level)+tc.ENDC+(" "*(11-len(str(player.level))))+"│"
            elif line == 11: return "│ "+tc.BOLD+"DIRECTIONS         "+tc.ENDC+"│"
            elif line == 13: return "│ NORTH:  "+self.getdir(0, 1)+"│"
            elif line == 14: return "│ EAST:   "+self.getdir(1, 0)+"│"
            elif line == 15: return "│ SOUTH:  "+self.getdir(0, -1)+"│"
            elif line == 16: return "│ WEST:   "+self.getdir(-1, 0)+"│"

            else:            return "│                    │"

    def drawScreen(self):
        os.system('clear')
        t = "\n\n".join(self.data)

        new_body = ""
        lines = t.split("\n")

        for line in lines:
            if len(line) > 40:
                w = textwrap.TextWrapper(width=40, break_long_words=False)
                line = '\n'.join(w.wrap(line))

            new_body += '\n'+line

        nb = new_body.split('\n')

        color = ""

        k = nb[-20:]
        if len(k)<21:
            for i in range(len(k), 20):
                k.append("")

        color = ""

        print('\n'*((os.get_terminal_size()[1]-21)//2))
        buffer = " "*((os.get_terminal_size()[0]-66)//2)

        for i in range(len(k)):

            ansi_escape = re.compile(r'''
                \x1B  # ESC
                (?:   # 7-bit C1 Fe (except CSI)
                    [@-Z\\-_]
                |     # or [ for CSI, followed by a control sequence
                    \[
                    [0-?]*  # Parameter bytes
                    [ -/]*  # Intermediate bytes
                    [@-~]   # Final byte
                )
            ''', re.VERBOSE)

            withoutEscape = ansi_escape.sub('', k[i])

            print(buffer+color+k[i]+tc.ENDC+(" "*(42-(len(withoutEscape))))+self.getLine(i, False))

            difference = [li for li in difflib.ndiff(k[i], withoutEscape) if li[0] != ' ']
            if len(difference)>0: 
                d2 = ""
                for l in range(len(difference)):
                    d2 += difference[l].replace("- ", "")
                color = "\033"+d2.split("\x1b")[-1]

    def takeInput(self):

        self.drawCutscene()

        self.drawScreen()

        buffer = " "*((os.get_terminal_size()[0]-66)//2)

        if player.x == 0 and player.y == -3:

            if not player.won:

                self.data = []

                player.x = 100
                player.y = 100

                self.getlocdata(True, player.x, player.y) 
                self.drawScreen()

            else:

                if not player.dspc:
                
                    stars.draw_credits()
                    player.dspc = True
                    self.drawScreen()
                    self.data = []
                    self.getlocdata(True, player.x, player.y)

        if player.x == 101 and player.y == 119:

            self.drawScreen()
            inp = input(buffer+"The machine requires a coin. Do you want\n"+buffer+"to play (y/n) ")
            if inp.lower().strip() == "y":
                if player.gold>0:
                    player.gold -= 1
                    if sokoban.main() == "WIN" and player.vgturns == 0:
                        player.gold += 5
                        player.vgturns += 1
                        self.data.append("Several gold coins fall out of the coin slot, and you hurry to pick them up.\nNOTE: You only get a reward once.")

                else:
                    self.data.append(tc.FAIL+"You don't have enough money"+tc.ENDC)
            
            player.x = 101
            player.y = 118

            self.getlocdata(False, player.x, player.y)

            self.drawScreen()
    
        else:

            player.write_vars(name)

            inp = input("\n"+buffer+"> ")

            if player.shop:
                if inp == "quit" or inp == "exit":
                    player.shop = False
                    self.data = []
                    self.getlocdata(True, player.x, player.y)

                elif inp.split(" ")[0] == "buy":
                    i = inp.replace(inp.split(" ")[0],"").strip()
                    if i == "life boost":
                        if player.gold<5:
                            self.data.append(tc.FAIL+"You don't have enough gold"+tc.ENDC)
                        else:
                            player.health += 20
                            self.data.append("Health increased by 20")
                            player.gold -= 5
                    elif i == "super life boost":
                        if player.gold<10:
                            self.data.append(tc.FAIL+"You don't have enough gold"+tc.ENDC)
                        else:
                            player.health += 50
                            self.data.append("Health increased by 50")
                            player.gold -= 10
                    else:
                        self.data.append(tc.FAIL+"You can't buy that"+tc.ENDC)

                else:
                    self.data.append(tc.FAIL+"You can't do that in a shop"+tc.ENDC)
            
            else:

                if inp in list(land.cheats):
                    z = land.cheats[inp]
                    player.level = list(land.cheats).index(inp)+1
                    player.x = z[0]
                    player.y = z[1]

                elif inp in list(self.autoreply):
                    self.data.append(self.autoreply[inp])

                else:

                    inp = inp.strip().lower()

                    inp = " "+inp+" "

                    for i in range(len(list(self.sub))):
                        if " "+list(self.sub)[i]+" " in inp: 
                            inp = inp.replace(list(self.sub)[i], self.sub[list(self.sub)[i]])

                    inp = inp.strip()

                    if inp == "":
                        self.data.append(tc.FAIL+"Beg pardon?"+tc.ENDC)
                    
                    else:

                        inp2 = inp.split(" ")

                        if inp in self.spesh:
                            if inp == "look":
                                self.getlocdata(True, player.x, player.y)
                            elif inp == "help":
                                self.data.append(self.helpcmd)
                            elif inp == "inventory":
                                self.data.append(tc.BOLD+"INVENTORY\n"+tc.ENDC+tc.OKBLUE+"- "+"\n- ".join(player.inv)+tc.ENDC)
                            elif inp == "clear":
                                self.data = []
                            elif inp == "exit" or inp == "quit":
                                global br
                                br = True
                            elif inp == "loc":
                                self.data.append(str(player.x)+" "+str(player.y))
                            elif inp == "shop":
                                if tuple([player.x, player.y]) in cut_data.cutcom:
                                    self.data = []
                                    self.data.append("You open a door, and enter the shop.")
                                    self.data.append("Type 'buy [item]' to buy something, and 'quit' to exit.")
                                    self.data.append(tc.BOLD+"ITEMS"+tc.ENDC+tc.OKCYAN+"\nLife Boost - 5\nSuper life boost - 10"+tc.ENDC)
                                    player.shop = True
                                else:
                                    self.data.append(tc.FAIL+"I don't see a shop here"+tc.ENDC)

                        else:

                            if len(inp2)<2:
                                self.data.append(tc.FAIL+"Use two-word commands, such as 'go north' or 'open door'"+tc.ENDC)

                            else:

                                if inp2[0] in self.sub:
                                    inp2[0] = self.sub[inp2[0]]

                                if inp2[1] in self.sub:
                                    inp2[1] = self.sub[inp2[1]]

                                if inp2[0] in self.begin:
                                    if inp.replace(inp2[0]+" ","") in self.end or inp.replace(inp2[0]+" ","") in list(self.items):
                                        self.parseInp([inp2[0], inp.replace(inp2[0]+" ","")])
                                    else:
                                        self.data.append(tc.FAIL+"I'm not quite sure what '"+inp.replace(inp2[0]+" ","")+"' is"+tc.ENDC)

                                elif inp2[0] == "take":
                                    if inp2[1] in list(self.items):
                                        self.parseInp([inp2[0], inp.replace(inp2[0]+" ","")])
                                    else:
                                        self.data.append(tc.FAIL+"'"+inp2[1]+"' doesn't exist"+tc.ENDC)

                                else:
                                    self.data.append(tc.FAIL+"I'm not quite sure what '"+inp.replace(inp2[0]+" ","")+"' means"+tc.ENDC)

                z = self.getproperty(player.x, player.y)  
                if "damage" in z:
                    if "the cold" == z['damage']:
                        if not "sweater" in player.ineffect:
                            dmg = random.randint(3, 5)
                            player.health -= dmg
                            self.data.append(tc.WARNING+"You take "+str(dmg)+" damage from "+z['damage']+tc.ENDC)

                    elif "water" == z['damage']:
                        dmg = 10
                        player.health -= dmg
                        self.data.append(tc.WARNING+"You take "+str(dmg)+" damage from "+z['damage']+tc.ENDC)
                    else:
                        self.data.append(tc.WARNING+"You take "+str(z['d'])+" damage from "+z['damage']+tc.ENDC)
                        player.health -= z['d']
                        player.x = player.oldx
                        player.y = player.oldy

                if player.health < 0:
                    self.data = [self.data[-1]]

                    self.data.append(tc.FAIL+"==== YOU DIED ===="+tc.ENDC)

                    player.health = 100
                    player.x = cut_data.cutcom[player.level-2][0]
                    player.y = cut_data.cutcom[player.level-2][1]
                    self.getlocdata(True, player.x, player.y)

                if player.inv.count("Shard part") >= 4:
                    player.inv.append("Blue shard")
                    self.data.append("The four shard parts seem to glow incredibly bright, floating and arranging themselves and forming the blue shard.")
                    for i in range(player.inv.count("Shard part")): del player.inv[player.inv.index("Shard part")]

                if "White shard" in player.inv and "Yellow shard" in player.inv and "Black shard" in player.inv and "Blue shard" in player.inv and "Green shard" in player.inv:
                    player.inv.append("Crystal")
                    player.x = 200
                    player.y = 200

                    del player.inv[player.inv.index("Green shard")]
                    del player.inv[player.inv.index("Blue shard")]
                    del player.inv[player.inv.index("Black shard")]
                    del player.inv[player.inv.index("Yellow shard")]
                    del player.inv[player.inv.index("White shard")]

                    self.drawCutscene()

            if player.x == 1000 and player.y == 1000:
                self.drawCutscene()
                
                player.x = 0
                player.y = -2
                player.inv.append("Ticket")
                self.data = []
                self.getlocdata(True, player.x, player.y)
                land.doors[str([[0, -2],[0, -3]])]['open'] = False

            if player.x == 100 and player.y == 108 and not land.riddleAns:
                self.data.append("As you walk closer to the shack, a man emerges. He makes a swiping motion with his hand, and a previously hidden door slides shut behind him. He glares at you, then decides to speak.")
                self.data.append('"Answer this riddle, and journey farther."'+tc.OKCYAN+'''\n\n"What grows louder the farther it rolls?"'''+tc.ENDC)

                self.drawScreen()  
                
                inp = input("\n"+buffer+"> ")
                if ("thunder") in inp.strip().lower():
                    self.data.append('''The door opens, and the man smiles. "Thank you for humoring me, adventurer. Perhaps now I can finally rest." You see an odd disturbance in the air, and the man is gone in a gust of wind. Perhaps it's only a trick of the light.''')

                    land.riddleAns = True

                    self.getlocdata(False, player.x, player.y)

                else:
                    player.x = 99
                    player.y = 104
                    self.data.append("The man frowns, and makes a snapping motion with his hands. Suddenly, a sizable portal opens. The portal has immense suction. You attempt to resist it, but you fail and fall in.")
                    self.getlocdata(False, player.x, player.y)



def get_players():
    players = os.listdir(directory.replace("Assets","Data"))
    for i in range(len(players)):players[i] = players[i].replace(".json","")

    if ".DS_Store" in players: del players[players.index(".DS_Store")]

    if len(players)==0: players=["None"]

    return players

def menu_inp():

    players = get_players()

    data = ['Type your username to log in, new ','[username] to create a new account and ', 'delete [username] to delete one.','',"Type 'quit' to quit",""]

    if players == ["None"]:
        data.append("It looks like you don't have")
        data.append("any accounts. Type 'new -d'")
        data.append("and we'll create one for you.'")

    while True:
        d = data[-20:]
        buffer = " "*((os.get_terminal_size()[0]-66)//2)

        os.system('clear')
        print('\n'*((os.get_terminal_size()[1]-21)//2))



        for q in range(20):
            if q >= len(d): 
                print(buffer+str(" "*42)+"  "+lang.getLine(q, True))
            else:
                print(buffer+data[q]+(" "*(42-len(data[q]))+"  "+lang.getLine(q, True)))


        inp = input("\n"+buffer+"> ")
        inp = inp.strip().lower()

        if "quit" in inp:
            os.system("clear")
            print("Bye!\n")
            quit()

        if inp in players:
            player.update_vars(inp)
            return inp

        elif len(inp.split(" ")) <=1:
            data.append("")
            data.append("That user doesn't exist")
        
        elif inp.split(" ")[0] == "new":
            if inp.split(" ")[1] == "-d":
                inp = "new "+str(pathlib.Path.home()).split("/")[-1].split("\\")[-1]

            if inp.split(" ")[1] in players:
                data.append("")
                data.append("That user already exists")

            else:
                player.reset_vars()
                player.write_vars(inp.split(" ")[1])
                player.update_vars(inp.split(" ")[1])
                players = get_players()
                return inp.split(" ")[1]

        elif inp.split(" ")[0] == "delete":
            if not inp.split(" ")[1] in players:
                data.append("")
                data.append("That user doesn't exist")

            else:

                os.remove(os.path.join(directory.replace("Assets","Data"), inp.split(" ")[1]+".json"))

                data.append("")
                data.append("User "+inp.split(" ")[1]+" removed")

                players = get_players()

        else:
            data.append("Unknown command")

lang = Lang()
stars.draw(5)

while True:
    lang.data = []
    
    name = menu_inp() 

    br = False

    lang.getlocdata(True, player.x, player.y)
    lang.data.append("Type 'help' for help")
    
    while br == False:
        lang.takeInput()
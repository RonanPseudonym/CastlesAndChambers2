import os, json, land
directory = os.path.dirname(os.path.realpath(__file__))

global inv, x, y, oldx, oldy, health, level, gold, ineffect, vgturns

inv = ["Letter","Wrapper"]

x = 0
y = 0
oldx = 0
oldy = 0

health = 100
level = 1
gold = 0
ineffect = []

vgturns = 0
won = False
dspc = False

shop = False

def reset_vars():

    inv = ["Letter","Wrapper"]

    x = 0
    y = 0
    oldx = 0
    oldy = 0

    health = 100
    level = 1
    gold = 0
    ineffect = []

    vgturns = 0
    won = False
    dspc = False

reset_vars()

def update_vars(name):
    f = open(os.path.join(directory.replace("Assets","Data"), name+".json"), "r")

    data = json.loads(f.read())
    f.close()

    global inv, x, y, oldx, oldy, health, level, gold, ineffect, vgturns
    inv = data['inv']
    x = data['x']
    y = data['y']
    oldx = data['oldx']
    oldy = data['oldy']
    health = data['health']
    level = data['level']
    gold = data['gold']
    ineffect = data['ineffect']
    vgturns = data['vgturns']
    land.all = data['land']
    land.doors = data['doors']
    won = data['won']
    dspc = data['dspc']

def write_vars(name):
    f = open(os.path.join(directory.replace("Assets","Data"), name+".json"), "w")

    f.write(json.dumps({
        "inv": inv,
        "x": x,
        "y": y,
        "oldx": oldx,
        "oldy": oldy,
        "health": health,
        "level": level,
        "gold": gold,
        "ineffect": ineffect,
        "vgturns": vgturns,
        "land": land.all,
        "won": won,
        "doors": land.doors,
        "dspc": dspc,
    }))

    f.close()

def print_inv():
    print(inv)
    quit()
import json
import os
import random
import threading
import time
import keyboard
from colorama import Fore

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import mixer
from musicEngine import musicEngine
from mapGenerator import mapGenerator

# keyboard.press('f11')
os.system("mode 800")

# some people meight be confused why am i clearing empty window on start with cls its beacuse
# if you dont do this the text cant be color just wold look like 53dtest insted of colored text
os.system("cls")

# init the mixer for it to work not sure if its needed i do it
mixer.init()

# just decoration line
cr = "+" + "-" * 234 + "+"

# set volumes
max_vol = 1
min_vol = 0.01
curr_vol = 0.01

# class for player
class player:
    def __init__(self):
        self.position = ""


alive = True
p = player()
mE = musicEngine()

mapGen = mapGenerator(current_level=1, preset="abcdefghijk")  # change preset to make map bigger/smaller
mapGen.generate_map(debugger=False)
mapGen.generate_bioms(debugger=False)

with open(f"map.json", "w") as save:
    json.dump(mapGen.map, save)


def starting_pos(debugger=False):
    """
    :param debugger: Bool : T/F if you want to see debugger info for normal game False
    :return:
    """
    if debugger:
        start = time.time()
    while True:
        rand = random.choice(mapGen.alphabet) + str(random.randint(1, len(mapGen.alphabet)))
        if mapGen.map[rand]["biom"] != "box":
            if mapGen.map[rand]["biom"] != "destination":
                if debugger:
                    print("setting random position too", round(time.time() - start, 10) * 1000, "ms")
                return rand


mE.MUSIC_STATE = "normal"
mE.vol = 0.01


def start_threads():
    # starts music engine as thread so the game can run
    song_thread = threading.Thread(target=music_player)
    song_thread.start()
    time.sleep(0.2)
    main_menu()


def die():
    # kills all threads
    global alive
    alive = False


def music_player():
    global alive
    while True:
        if not alive:
            break
        engine = mE.start()
        if engine == "NoDirSong":
            print("no songs in current_folder/music/normal turning off music engine")
            break


def setting_menu():
    global curr_vol
    global alive
    print(cr)
    print("\u001b[37m[\u001b[32m1\u001b[37m] Music volume")
    print("")
    print("\u001b[37m[\u001b[32mB\u001b[37m] Back")
    print(cr)
    setting_menu_input = input("> ").lower().strip()
    if setting_menu_input == "1":
        os.system("cls")
        print("set volume for music max is", max_vol, "min is", min_vol, "current is", curr_vol)
        music_set_input = input("> ").lower().strip()
        music_set = float(music_set_input)
        if music_set > max_vol:
            print("way too high volume")
            time.sleep(2)
            os.system("cls")
            setting_menu()
        if music_set < 0:
            print("volume must be positive number if you dont want the music set the volume to 0")
            time.sleep(2)
            os.system("cls")
            setting_menu()
        mE.vol = music_set
        curr_vol = music_set
        os.system("cls")
        setting_menu()
    if setting_menu_input == "b":
        os.system("cls")
        main_menu()


def main_menu():
    print(cr)
    print("""
  _____               _                                   
 |  __ \             | |                                  
 | |__) |   _ _______| | ___    __ _  __ _ _ __ ___   ___ 
 |  ___/ | | |_  /_  / |/ _ \  / _` |/ _` | '_ ` _ \ / _ \\
 | |   | |_| |/ / / /| |  __/ | (_| | (_| | | | | | |  __/
 |_|    \__,_/___/___|_|\___|  \__, |\__,_|_| |_| |_|\___|
                                __/ |                     
                               |___/   
""")
    print(cr)
    print("\u001b[37m[\u001b[32m1\u001b[37m] Start")
    print("\u001b[37m[\u001b[32m2\u001b[37m] Settings")
    print("\u001b[37m[\u001b[32m3\u001b[37m] Credits")
    print("")
    print("\u001b[37m[\u001b[32mX\u001b[37m] Close game")
    print(cr)
    main_menu_input = input("> ").lower().strip()
    if main_menu_input == "1":
        os.system("cls")
        moving()
    if main_menu_input == "2":
        os.system("cls")
        setting_menu()
    if main_menu_input == "3":
        os.system("cls")
        credits_menu()
    if main_menu_input == "x":
        die()
        mixer.quit()
        exit()
    else:
        os.system("cls")
        main_menu()


def credits_menu():
    print(cr)
    print("This game is made by jonasek369")
    print(cr)
    print("\u001b[37m[\u001b[32mB\u001b[37m] Back")
    print(cr)

    credits_menu_input = input("> ").lower().strip()
    if credits_menu_input == "b":
        os.system("cls")
        main_menu()


def check_for_boxes():
    boxes = 0
    locked_boxes = 0
    destination = 0

    for i in mapGen.map:
        if mapGen.map[i]["biom"] == "box":
            boxes += 1

        if mapGen.map[i]["biom"] == "locked_box":
            locked_boxes += 1

        if mapGen.map[i]["biom"] == "destination":
            destination += 1
    if boxes == 0 and locked_boxes == mapGen.max_boxes:
        return True
    else:
        return False


def collision_check(direction):
    """
    :param direction: Str : example up
    :return:
    """

    # really scuffed needs hard rework worked on this in night and its bad
    # but it dose its job so i guess its ok for now
    if mapGen.map[p.position][direction] is not None:
        if mapGen.map[mapGen.map[p.position][direction]]["biom"] != "locked_box":
            if mapGen.map[mapGen.map[p.position][direction]] is not None:
                if mapGen.map[mapGen.map[p.position][direction]]["biom"] == "box":
                    if mapGen.map[mapGen.map[p.position][direction]][direction] is not None:
                        if mapGen.map[mapGen.map[mapGen.map[p.position][direction]][direction]]["biom"] == "box":
                            return False
                    if mapGen.map[mapGen.map[p.position][direction]][direction] is not None:
                        if mapGen.map[mapGen.map[mapGen.map[p.position][direction]][direction]]["biom"] == "locked_box":
                            return False
                    if mapGen.map[mapGen.map[p.position][direction]][direction] is not None:
                        if mapGen.map[mapGen.map[mapGen.map[p.position][direction]][direction]]["biom"] == "destination":
                            mapGen.map[mapGen.map[mapGen.map[p.position][direction]][direction]]["biom"] = "locked_box"
                            mapGen.map[mapGen.map[p.position][direction]]["biom"] = "land"
                            p.position = mapGen.map[p.position][direction]
                            return True

                        else:
                            mapGen.map[mapGen.map[mapGen.map[p.position][direction]][direction]]["biom"] = "box"
                            mapGen.map[mapGen.map[p.position][direction]]["biom"] = "land"
                            p.position = mapGen.map[p.position][direction]
                            return True
                else:
                    p.position = mapGen.map[p.position][direction]
        else:
            return False


def currently_playing(song, rainbow=False):
    """
    :param rainbow: Bool : rainbow effect not the best but for fun why not
    :param song: Str : Song name
    :return:
    """
    # formats song name (just removes extension for now)
    formated = ""
    colors = [
        Fore.RED,
        Fore.GREEN,
        Fore.YELLOW,
        Fore.BLUE,
        Fore.MAGENTA,
        Fore.CYAN,
        Fore.WHITE,
        Fore.LIGHTBLACK_EX,
        Fore.LIGHTRED_EX,
        Fore.LIGHTGREEN_EX,
        Fore.LIGHTYELLOW_EX,
        Fore.LIGHTBLUE_EX,
        Fore.LIGHTMAGENTA_EX,
        Fore.LIGHTCYAN_EX,
        Fore.LIGHTWHITE_EX
    ]
    extension = [
        ".mp3",
        ".wav",
        ".ogg"
    ]
    for exts in extension:
        if exts in song:
            formated = song.replace(exts, "")

    if len(song) == 0:
        formated = song
    if rainbow:
        ranb = ""
        for i in formated:
            ranb += random.choice(colors) + i + Fore.WHITE
        return ranb
    else:
        return formated


def moving():
    # main gameplay fuction
    global alive, newpos_save
    while True:
        win = check_for_boxes()
        if win:
            os.system("cls")
            print(cr)
            print("you completed", mapGen.max_boxes, "level")
            print(cr)
            mapGen.create_new_level()
            time.sleep(0.5)
            with open(f"map.json", "w") as save:
                json.dump(mapGen.map, save)
            newpos_save = p.position
        else:
            pass
        os.system("cls")
        print("your position", p.position, "level", mapGen.max_boxes)
        print("playing:", currently_playing(mE.currently_playing["name"], rainbow=False))
        print(cr)
        print(mapGen.show_map(p.position))
        print(cr)
        print("\u001b[37m[\u001b[32mW\u001b[37m] Forward")
        print("\u001b[37m[\u001b[32mA\u001b[37m] Left")
        print("\u001b[37m[\u001b[32mS\u001b[37m] Down")
        print("\u001b[37m[\u001b[32mD\u001b[37m] Right")
        print("\u001b[37m[\u001b[32mR\u001b[37m] Reset")
        print("\u001b[37m[\u001b[32mB\u001b[37m] Back to menu")
        print(cr)
        time.sleep(0.15)  # refresh time
        wait_until_play()


def wait_until_play():
    # waits until player press some button i use this so the command line doesn't flicker
    while True:
        if keyboard.is_pressed("b"):
            os.system("cls")
            main_menu()

        if keyboard.is_pressed("w"):
            collision_check("up")
            return

        if keyboard.is_pressed("a"):
            collision_check("left")
            return

        if keyboard.is_pressed("s"):
            collision_check("down")
            return

        if keyboard.is_pressed("d"):
            collision_check("right")
            return

        if keyboard.is_pressed("r"):
            if mapGen.max_boxes == 1:
                mapGen.map.clear()
                p.position = oldppos
                with open("map.json", "r") as rd:
                    mapGen.map = json.loads(rd.read())
                return
            else:
                mapGen.map.clear()
                p.position = newpos_save
                with open("map.json", "r") as rd:
                    mapGen.map = json.loads(rd.read())
                return


# creates starting pos saves it and start all threads
p.position = starting_pos()
oldppos = p.position
start_threads()

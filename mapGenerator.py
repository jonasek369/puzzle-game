import time
import random
from colorama import Fore

class mapGenerator:
    def __init__(self, current_level, preset="abcdefghij"):
        # preset needs to start with A
        self.map = dict()
        self.biom_info = {"land": 0, "box": 0, "destination": 0}
        self.torf = [
            True,
            False
        ]
        self.max_boxes = current_level
        self.alphabet = list(preset)

        self.borders = []

        for i in range(len(self.alphabet)):
            self.borders.append(f"a{i + 1}")
        for i in self.alphabet:
            self.borders.append(f"{i}1")
        for i in range(len(self.alphabet)):
            self.borders.append(f"{self.alphabet[len(self.alphabet) - 1]}{i + 1}")
        for i in self.alphabet:
            self.borders.append(f"{i}{len(self.alphabet)}")

        self.directions = [
            "up",
            "down",
            "left",
            "right"
        ]

        self.bioms = [
            "land",
            "box",
            "destination"
        ]

    def generate_map(self, debugger=False):
        if debugger:
            start = time.time()
        for pos, x in enumerate(self.alphabet):
            for y in range(len(self.alphabet)):
                y = y + 1

                up, down, left, right = self.create_cords_for_axies(x, y, pos)

                self.map[f"{x}{y}"] = {
                    "cords": f"{x}{y}",
                    "examined": False,
                    "biom": "",
                    "up": up,
                    "left": left,
                    "right": right,
                    "down": down
                }

        if debugger:
            print("generated map with layout of", self.alphabet, "took", round(time.time() - start, 10) * 1000, "ms")
            if round(time.time() - start, 10) * 1000 > 100:
                print("possible buffer overload")
        return self.map

    def generate_bioms(self, debugger=False):
        if debugger:
            start = time.time()
        self.biom_info["box"] = 0
        self.biom_info["destination"] = 0

        while self.biom_info["destination"] != self.max_boxes:
            if self.biom_info["box"] == self.max_boxes:
                break
            random_x = random.choice(self.alphabet)
            random_y = random.randint(1, len(self.alphabet))
            if self.map[f"{random_x}{random_y}"]["cords"] not in self.borders:
                if self.map[f"{random_x}{random_y}"]["biom"] == "":
                    self.map[f"{random_x}{random_y}"]["biom"] = "box"
                    self.biom_info["box"] += 1
                else:
                    continue
            else:
                continue

        while True:
            if self.biom_info["destination"] == self.max_boxes:
                break
            random_x = random.choice(self.alphabet)
            random_y = random.randint(1, len(self.alphabet))
            if self.map[f"{random_x}{random_y}"]["biom"] == "":
                self.map[f"{random_x}{random_y}"]["biom"] = "destination"
                self.biom_info["destination"] += 1
            else:
                continue

        # cleanup
        for i in self.map:
            if self.map[i]["biom"] == "":
                self.map[i]["biom"] = "land"
            else:
                continue

        if debugger:
            print("created bioms with set of", self.biom_info, "took", round(time.time() - start, 10) * 1000, "ms")

    def show_map(self, player_pos):
        form_map = ""
        for i in self.map:
            if self.map[i]["cords"] == player_pos:
                if str(len(self.alphabet)) in self.map[i]["cords"]:
                    form_map += Fore.MAGENTA + i + Fore.WHITE + "\n"
                    continue
                else:
                    form_map += Fore.MAGENTA + i + Fore.WHITE
                    continue

            if self.map[i]["biom"] == "land":
                if str(len(self.alphabet)) in self.map[i]["cords"]:
                    form_map += Fore.GREEN + i + Fore.WHITE + "\n"
                    continue
                else:
                    form_map += Fore.GREEN + i + Fore.WHITE
                    continue
            #
            if self.map[i]["biom"] == "box":
                if str(len(self.alphabet)) in self.map[i]["cords"]:
                    form_map += Fore.YELLOW + i + Fore.WHITE + "\n"
                    continue
                else:
                    form_map += Fore.YELLOW + i + Fore.WHITE
                    continue

            if self.map[i]["biom"] == "destination":
                if str(len(self.alphabet)) in self.map[i]["cords"]:
                    form_map += Fore.RED + i + Fore.WHITE + "\n"
                    continue
                else:
                    form_map += Fore.RED + i + Fore.WHITE
                    continue
            #
            if self.map[i]["biom"] == "locked_box":
                if str(len(self.alphabet)) in self.map[i]["cords"]:
                    form_map += Fore.CYAN + i + Fore.WHITE + "\n"
                    continue
                else:
                    form_map += Fore.CYAN + i + Fore.WHITE
                    continue

            if str(len(self.alphabet)) in self.map[i]["cords"]:
                form_map += i + "\n"
                continue
            else:
                form_map += i
                continue

        return form_map

    def create_cords_for_axies(self, x, y, pos):
        if pos - 1 >= 0:
            try:
                up = str(self.alphabet[pos - 1]) + str(y)
            except IndexError:
                up = None
        else:
            up = None

        # down
        try:
            down = str(self.alphabet[pos + 1]) + str(y)
        except IndexError:
            down = None

        # left
        if len(self.alphabet) >= y - 1 > 0:
            left = x + str(y - 1)
        else:
            left = None

        # right
        if len(self.alphabet) >= y + 1 > 0:
            right = x + str(y + 1)
        else:
            right = None

        return up, down, left, right

    def create_new_level(self):
        self.map.clear()
        self.max_boxes += 1
        mapGenerator.generate_map(self, debugger=False)
        mapGenerator.generate_bioms(self, debugger=False)

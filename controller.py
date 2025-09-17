import inputs
import pyautogui
import threading

class Controller:
    def __init__(self):
        listener = threading.Thread(target=self.listen,daemon=True)
        #   pr, up, dn, lt, rt
        # N
        # U
        # R
        # D
        # L
        # P
        self.MAPPING = [
            # no lt/rt
            'e', 'o', 'a', 'i', 'u',
            'l', 't', 'h', 'r', 'd',
            'y', 'n', 's', 'm', 'w',
            'v', 'f', 'g', 'p', 'b',
            'c', 'k', 'j', 'x', 'z',
            "'", '.', ',', '-', 'q',
            # rt
            'E', 'O', 'A', 'I', 'U',
            'L', 'T', 'H', 'R', 'D',
            'Y', 'N', 'S', 'M', 'W',
            'V', 'F', 'G', 'P', 'B',
            'C', 'K', 'J', 'X', 'Z',
            '"', '!', '?', '/', 'Q',
            # lt
            '0', '1', '2', '3', '4',
            '5', '6', '7', '8', '9',
            '/', '$', '%', '[', ']',
            '&', '@', '#', '(', ')',
            ';', '=', ':', '<', '>',
            '+', '^', '*', '{', '}',
            # rt+lt
            'ē', 'ō', 'ā', 'ī', 'ū',
            '`', '', '', 'brb', 'ok',
            '\\', '', '', 'pls', 'thx',
            '~', '', '', 'idk', 'lol',
            '_', '', '', 'yes', 'no',
            '|', '', '', 'hi', 'bye',
        ]
        self.keys = {
            "U":False,
            "L":False,
            "R":False,
            "D":False,
            "P":False,

            "LB":False,
            "RB":False,
        }
        self.plugged = False
        listener.start()

    def listen(self):
        ignore = 0
        while True:
            try:
                events:list[inputs.InputEvent] = inputs.get_gamepad()
                self.plugged = True
            except inputs.UnpluggedError:
                self.plugged = False
                continue
            for event in events:
                #print(event.code)
                if event.code == "BTN_TL":
                    if event.state == 1:
                        self.keys['LB'] = True
                    else:
                        self.keys['LB'] = False
                if event.code == "BTN_TR":
                    if event.state == 1:
                        self.keys['RB'] = True
                    else:
                        self.keys['RB'] = False

                if event.code == "ABS_HAT0X":
                    if event.state == 1:
                        pyautogui.press("right")
                    if event.state == -1:
                        pyautogui.press("left")
                if event.code == "ABS_HAT0Y":
                    if event.state == 1:
                        pyautogui.press("down")
                    if event.state == -1:
                        pyautogui.press("up")

                if event.code == "BTN_THUMBL":
                    if event.state == 1:
                        self.keys["P"] = True
                    else:
                        self.keys["P"] = False
                
                if event.code == "BTN_WEST" and event.state == 1:
                    pyautogui.press('backspace')
                if event.code == "BTN_SOUTH" and event.state == 1:
                    pyautogui.press('enter')
                if event.code == "BTN_NORTH" and event.state == 1:
                    pyautogui.press('space')

                if event.code == "BTN_THUMBR" and event.state == 1:
                    self.write(0)
                elif event.state > 2**14:
                    if event.code == "ABS_RY":
                        if ignore != 1:
                            ignore = 1
                            self.write(1)
                    elif event.code == "ABS_RX":
                        if ignore != 4:
                            ignore = 4
                            self.write(4)
                    else:
                        ignore = 0
                    
                    if event.code == "ABS_Y":
                        self.keys["U"] = True
                        self.keys["L"] = False
                        self.keys["R"] = False
                        self.keys["D"] = False
                    elif event.code == "ABS_X":
                        self.keys["U"] = False
                        self.keys["L"] = False
                        self.keys["R"] = True
                        self.keys["D"] = False

                elif event.state < -2**14:
                    if event.code == "ABS_RY":
                        if ignore != 2:
                            ignore = 2
                            self.write(2)
                    elif event.code == "ABS_RX":
                        if ignore != 3:
                            ignore = 3
                            self.write(3)
                    else:
                        ignore = 0
                    if event.code == "ABS_Y":
                        self.keys["U"] = False
                        self.keys["L"] = False
                        self.keys["R"] = False
                        self.keys["D"] = True
                    elif event.code == "ABS_X":
                        self.keys["U"] = False
                        self.keys["L"] = True
                        self.keys["R"] = False
                        self.keys["D"] = False
                elif event.code == "ABS_RY" or event.code == "ABS_RX":
                    ignore = 0

                if (abs(event.state) < 2**14) and (event.code == "ABS_X" or event.code == "ABS_Y"):
                    self.keys["U"] = False
                    self.keys["L"] = False
                    self.keys["R"] = False
                    self.keys["D"] = False
    
    def write(self, id):
        index = id + (5 if self.keys["U"] else 10 if self.keys["R"] else 15 if self.keys["D"] else 20 if self.keys["L"] else 25 if self.keys["P"] else 0)
        index += 30 if self.keys["RB"] else 0
        index += 60 if self.keys["LB"] else 0
        pyautogui.typewrite(self.MAPPING[index])

if __name__ == "__main__":
    controller = Controller()
    while 1: pass
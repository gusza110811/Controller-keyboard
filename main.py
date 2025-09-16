import tkinter as tk
import threading
import time
from controller import Controller

class PreviewWindow:
    def __init__(self, controller: Controller):
        self.controller = controller
        self.root = tk.Tk()
        self.root.title("Controller Typing")
        self.root.geometry("180x180")
        self.root.attributes("-toolwindow", True)
        self.root.attributes("-topmost", True)
        self.root.resizable = False

        self.label = tk.Label(self.root, text="", font=("Consolas", 30))
        self.label.pack(expand=True)

        self.update = threading.Thread(target=self.updateloop,daemon=True)
        self.update.start()

    def updateloop(self):
        while 1:
            index = (5 if self.controller.keys["U"] else
                    10 if self.controller.keys["R"] else
                    15 if self.controller.keys["D"] else
                    20 if self.controller.keys["L"] else
                    25 if self.controller.keys["P"] else 0)
            self.label.config(text=f"{self.controller.MAPPING[index+1]}\n{self.controller.MAPPING[index+3]} {self.controller.MAPPING[index]} {self.controller.MAPPING[index+4]}\n{self.controller.MAPPING[index+2]}")
            time.sleep(0.05)
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    controller = Controller()
    preview = PreviewWindow(controller)

    preview.run()

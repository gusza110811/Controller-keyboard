import tkinter as tk
from tkinter import scrolledtext
import threading
import time
import os
import sys
from controller import Controller

#This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.

#This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

#You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.

class GnuNotice:
    def __init__(self):
        self.agree = os.path.exists(".agree")
        if self.agree:
            return
        with open(".agree","w") as agree:
            agree.write("If you choose to stop agreeing to the terms and conditions, you are free to uninstall the software")
        with open("LICENSE") as license:
            self.file = license.read()
        self.root = tk.Tk()
        self.root.title("Terms and Conditions")
        self.text = scrolledtext.ScrolledText(self.root)
        self.text.insert(tk.END,self.file)
        self.text.config(state="disabled")
        self.text.pack()

        self.label = tk.Label(self.root,text="By continuing to use this software,\nyou agree to the license above", font=("Helvetica","15"))
        self.label.pack()

        self.main()

    def main(self):
        self.root.mainloop()

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
    import makelicense
    makelicense.makeLicense()
    controller = Controller()
    preview = PreviewWindow(controller)
    
    notice = threading.Thread(target=lambda:GnuNotice(), daemon=False)
    notice.start()

    preview.run()

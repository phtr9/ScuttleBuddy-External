import tkinter as tk
import time
from typing import Callable, Any


# https://github.com/notatallshaw/fall_guys_ping_estimate/blob/main/fgpe/overlay.py


class Overlay:
    def __init__(self,
                 camp_names,
                 cheat,
                 get_new_text_callback):

        self.camp_names = camp_names
        self.cheat = cheat
        self.get_new_text_callback = get_new_text_callback

        self.root = tk.Tk()

        # Define Window Geometry
        self.root.overrideredirect(True)
        self.root.geometry("+5+5")
        self.root.lift()
        self.root.wm_attributes("-topmost", True)
        self.root.wm_attributes("-transparentcolor", 'grey19')

        self.set_attributes()

    def set_attributes(self):
        for n, camp_name in enumerate(self.camp_names):
            setattr(self, f"{camp_name}_text", tk.StringVar())
            text = getattr(self, f"{camp_name}_text")

            setattr(self, f"{camp_name}_label", self.create_label(text))
            label = getattr(self, f"{camp_name}_label")
    
            label.grid(row=0, column=n)

    def create_label(self, text):
        return tk.Label(self.root,
                        textvariable=text,
                        font=('Consolas', '14'),
                        fg='green3',
                        bg='grey19')

    def update_label(self):
        if self.cheat:
            for jungle_camp, jungle_info in self.get_new_text_callback().items():
                text = getattr(self, f"{jungle_camp}_text")
                text.set(f'| {jungle_camp}: {jungle_info["timer"]}')
            self.root.after(1, self.update_label)
        else:
            for jungle_camp, respawn_time in self.get_new_text_callback().items():
                text = getattr(self, f"{jungle_camp}_text")
                text.set(f'| {jungle_camp}: {respawn_time}')
            self.root.after(1, self.update_label)

    def run(self):
        for camp_name in self.camp_names:
            text = getattr(self, f"{camp_name}_text")
            text.set(f'| {camp_name}: --:--')

        self.root.after(1, self.update_label)
        self.root.mainloop()

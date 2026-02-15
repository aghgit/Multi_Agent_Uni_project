import threading
import time

import pyautogui
import pyperclip
from openai import OpenAI

from . import open_sticky_notes

"""
class NoteAgent:
    def __init__(self, intent):
        open_sticky_notes.open_sticky_notes_shell()
        pyautogui.PAUSE = 0.5
        time.sleep(0.5)
        pyautogui.hotkey("ctrl", "n")
        time.sleep(0.5)
        pyperclip.copy("Please wait for LLM output.")
        pyautogui.hotkey("ctrl", "v")
        pyperclip.copy(intent["query"])
        pyautogui.hotkey("ctrl", "a")
        pyautogui.hotkey("del")

        pyautogui.hotkey("ctrl", "v")

        pyautogui.hotkey("alt", "f4")

        pyautogui.hotkey("alt", "f4")
"""


class NoteAgent:
    def __init__(self):
        pass

    def run(self, intent):
        open_sticky_notes.open_sticky_notes_shell()
        pyautogui.PAUSE = 0.5
        time.sleep(0.5)
        pyautogui.hotkey("ctrl", "n")
        time.sleep(0.5)
        pyperclip.copy("Please wait for LLM output.")
        pyautogui.hotkey("ctrl", "v")
        pyperclip.copy(intent["query"])
        pyautogui.hotkey("ctrl", "a")
        pyautogui.hotkey("del")

        pyautogui.hotkey("ctrl", "v")

        pyautogui.hotkey("alt", "f4")
        pyautogui.hotkey("alt", "f4")

        return {"type": "success", "data": "Note Created"}

import tkinter as tk

import pyperclip
import pytesseract
from PIL import Image
import mss
from pynput import keyboard

activate_flag = False
quit_flag = False
_root = None


def on_activate():
    global activate_flag
    activate_flag = True


def on_quit():
    global quit_flag
    quit_flag = True


class Overlay:
    def __init__(self, master):
        self.master = master
        self.top = tk.Toplevel(master)
        self.top.overrideredirect(True)
        self.top.attributes('-topmost', True)
        self.top.attributes('-alpha', 0.3)
        self.top.configure(bg='gray')

        with mss.mss() as sct:
            m = sct.monitors[0]
        self.top.geometry(f"{m['width']}x{m['height']}+{m['left']}+{m['top']}")
        self._screen = m

        self.canvas = tk.Canvas(self.top, bg='gray',
                                highlightthickness=0, borderwidth=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.start_canvas_x = self.start_canvas_y = None
        self.start_root_x = self.start_root_y = None
        self.rect = None

        self.canvas.bind("<ButtonPress-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_move)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)
        self.top.bind("<Escape>", lambda e: self.cancel())

    def on_mouse_down(self, event):
        self.start_canvas_x = event.x
        self.start_canvas_y = event.y
        self.start_root_x = event.x_root
        self.start_root_y = event.y_root
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(
            event.x, event.y, event.x, event.y,
            outline='red', width=2, dash=(5, 2)
        )

    def on_mouse_move(self, event):
        if self.rect:
            self.canvas.coords(
                self.rect,
                self.start_canvas_x, self.start_canvas_y,
                event.x, event.y
            )

    def on_mouse_up(self, event):
        PAD = 8
        m = self._screen
        sl, st = m["left"], m["top"]
        sw, sh = sl + m["width"], st + m["height"]
        x1 = max(sl, min(self.start_root_x, event.x_root) - PAD)
        y1 = max(st, min(self.start_root_y, event.y_root) - PAD)
        x2 = min(sw, max(self.start_root_x, event.x_root) + PAD)
        y2 = min(sh, max(self.start_root_y, event.y_root) + PAD)
        self.top.withdraw()
        try:
            text = self._ocr(x1, y1, x2, y2)
            if text.strip():
                pyperclip.copy(text.strip())
                print("Copied to clipboard.")
            else:
                print("No text found.")
        except Exception as e:
            print(f"OCR error: {e}")
        finally:
            self.cleanup()

    def _ocr(self, x1, y1, x2, y2):
        if x2 <= x1 or y2 <= y1:
            return ""
        with mss.mss() as sct:
            shot = sct.grab({"left": x1, "top": y1,
                             "width": x2 - x1, "height": y2 - y1})
            img = Image.frombytes("RGB", shot.size, shot.bgra, "raw", "BGRX")
        return pytesseract.image_to_string(img)

    def cancel(self):
        self.cleanup()

    def cleanup(self):
        global activate_flag
        if self.rect:
            self.canvas.delete(self.rect)
        self.top.destroy()
        activate_flag = False


def _check_activation():
    global activate_flag, quit_flag, _root
    if quit_flag:
        _root.quit()
        return
    if activate_flag:
        Overlay(_root)
        activate_flag = False
    _root.after(100, _check_activation)


def main():
    global _root
    listener = keyboard.GlobalHotKeys({
        '<ctrl>+<shift>+c': on_activate,
        '<ctrl>+<shift>+q': on_quit,
    })
    listener.start()
    print("screen-ocr running. Ctrl+Shift+C to capture, Ctrl+Shift+Q to quit.")

    _root = tk.Tk()
    _root.withdraw()
    _root.after(100, _check_activation)
    _root.mainloop()


if __name__ == "__main__":
    main()

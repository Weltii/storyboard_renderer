import tkinter
import tkinter.font as font

from backend.utils.utils import open_browser


class Gui(tkinter.Tk):
    head: tkinter.Label
    status: tkinter.Label
    open_browser_button: tkinter.Button

    def __init__(self):
        super().__init__()
        self.title("Storyboard Renderer")

        # add headline
        self.head = tkinter.Label(
            self,
            text="Storyboard Renderer Backend Log",
            font=tkinter.font.Font(size="20"),
        )
        self.head.pack()

        self.status = tkinter.Label(
            self,
            text="Storyboard Renderer is running! Don't close this window while you work with the tool!",
        )
        self.status.pack()

        self.open_browser_button = tkinter.Button(
            self, text="Open Storyboard-Renderer in browser", command=open_browser
        )
        self.open_browser_button.pack()

        self.mainloop()


if __name__ == "__main__":
    gui = Gui()

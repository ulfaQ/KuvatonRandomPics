from tkinter import Tk, Label
from bs4 import BeautifulSoup
from urllib.request import urlopen
from PIL import Image, ImageTk
import PIL
from io import BytesIO
from threading import Thread
import threading
import re, time

class CustList(list):

    def __init__(self, instance):

        while True:
            linkit = instance.give_me_links(instance.url)
            if linkit:
                break

        linkit_setti = set()

        for i in linkit:
            if "browse" in i:
                linkit_setti.add(i)

        return super().__init__(list(linkit_setti)) # Might as well use a set in the rest of the script


    def pop(self, instance):

        if len(self) < 2:
            self.__init__(instance)

        return super().pop()


class Main():

    """ gets urls from kuvaton.com/1/rand, those urls are not images but links 
    to pages containing those images. After this we get the real images from those urls.
    We then show the user a different image everytime she/he presses a key (any key/mouse button) """

    def __init__(self):
        self.root = Tk() 
        self.url = "http://www.kuvaton.com/1/rand/"
        self.root.attributes("-zoomed", True)
        self.root.configure(bg="black")
        self.image_panel = Label(self.root, text="Press Any Key", bg="black")
        self.image_panel.bind("<Key>", self.show_image)
        self.image_panel.bind("<Button>", self.show_image)
        self.image_panel.pack()
        self.image_panel.focus_force()
        self.next_queue = CustList(self)

        self.root.mainloop()

    def give_me_links(self, url):
        url_to_open, pattern = urlopen(url), "http://[a-zA-Z0-9\.\/]*\.jpg" # Try this [.] insted of this[a-zA-Z0-9\.\/]
        print("got links from {}".format(url))
        return re.findall(pattern, BeautifulSoup(url_to_open, "lxml").decode())

    def show_image(self, event=None):

        self.image_panel.configure(height=self.root.winfo_height())
        self.image_panel.unbind("<Key>")

        def set_current_image():
            ready_image = ImageTk.PhotoImage(give_resized_image(Image.open(BytesIO(urlopen(self.next_image).read()))))
            self.image_panel.configure(image=ready_image)
            self.image_panel.image = ready_image

        def set_next_image(event=None):
            for i in threading.enumerate():
                print(i)
            kuva_urlit = self.give_me_links(self.next_queue.pop(self))

            for url in kuva_urlit:
                if "kuvei" in url:
                    kuva = url
                    break

            print("got pic link", kuva)
            self.image_panel.bind("<Key>", self.show_image)
            self.next_image = kuva

        def give_resized_image(img):
            window_height = self.root.winfo_height()
            if img.size[0] > window_height:
                width = (float(img.size[0]) * float((window_height / float(img.size[1]))))
                return img.resize((int(width), window_height), PIL.Image.ANTIALIAS)
            else: 
                return img

        try:
            set_current_image()
        except AttributeError:
            set_next_image()
            set_current_image()

        self.thread =  Thread(target=set_next_image)
        self.thread.start()

if __name__ == "__main__":
    main = Main()

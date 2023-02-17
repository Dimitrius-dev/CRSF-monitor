import threading
import tkinter
from random import random
from threading import Thread, Event
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showerror

from SerialReader import SerialReader


class Client:
    def __init__(self):
        self.__t = None
        self.__event = threading.Event()
        self.__event.set()

        self.__btn_start = None
        self.__btn_stop = None

        self.__window = Tk()
        self.__window.title("CRSF monitor")
        self.__window.geometry('650x530')
        self.__window.resizable(False, False)

        self.__list_channels = []
        for i in range(16):
            f = IntVar()
            f.set(random() * 60)
            # f.set(100)
            self.__list_channels.append(f)

        self.__setup_UI()

    def __setup_UI(self):
        self.__btn_start = Button(self.__window, text="start reading", command=self.__run_read_serial)
        self.__btn_start.grid(column=0, row=0, padx=10)

        self.__btn_stop = Button(self.__window, text="stop reading", command=self.__stop_read_serial)
        self.__btn_stop.grid(column=0, row=2, padx=10)
        self.__btn_stop["state"] = tkinter.DISABLED

        for i in range(16):
            lbl = Label(self.__window, text=f"channel #{i} HEX")
            lbl.grid(column=1, row=i, padx=1, pady=5)

            lbl = Label(self.__window, text=str(self.__list_channels[i].get()))
            lbl.grid(column=2, row=i, padx=1, pady=5)

            lbl = Label(self.__window, text=f"channel #{i}")
            lbl.grid(column=3, row=i, padx=1, pady=5)

            progressbar = ttk.Progressbar(self.__window, orient="horizontal", variable=self.__list_channels[i], length=300)
            progressbar.grid(column=4, row=i, padx=1, pady=5)


    def __run_read_serial(self):
        self.__event.clear()

        self.__t = Thread(target=self.__serial_handler).start()

        self.__btn_start["state"] = tkinter.DISABLED
        self.__btn_stop["state"] = tkinter.NORMAL

        print("start")

    def __stop_read_serial(self):
        self.__event.set()

        self.__btn_start["state"] = tkinter.NORMAL
        self.__btn_stop["state"] = tkinter.DISABLED

        print("stop")

    def __serial_handler(self):

        reader = None
        try:
            reader = SerialReader()
        except Exception as ex:
            showerror(title="Error", message="Serial is not available")
            return

        while not self.__event.is_set():
            channels = reader.parse()

            for i in range(16):
                print(f"channel #{i}", int(channels[i], 2)/20)
                self.__list_channels[i].set(int(channels[i], 2) / 20)

            print("\n\n")

    def start(self):
        self.__window.mainloop()
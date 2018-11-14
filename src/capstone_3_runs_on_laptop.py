"""
Mini-application:  Buttons on a Tkinter GUI tell the robot to:
  - Go forward at the speed given in an entry box.

This module runs on your LAPTOP.
It uses MQTT to SEND information to a program running on the ROBOT.

Authors:  David Mutchler, his colleagues, and Rui Fang.
"""

import tkinter
from tkinter import ttk
import mqtt_remote_method_calls as com
import time


def main():
    """ Constructs and runs a GUI for this program. """
    root = tkinter.Tk()

    mqtt_client = com.MqttClient()
    mqtt_client.connect('fr', 'robo32')

    setup_gui(root, mqtt_client)

    root.mainloop()


def setup_gui(root_window, client):
    """ Constructs and sets up widgets on the given window. """
    frame = ttk.Frame(root_window, padding=10)
    frame.grid()

    speed_entry_box = ttk.Entry(frame)
    go_forward_button = ttk.Button(frame, text="Go forward")
    top_red = ttk.Button(frame, text='Top Red', command=lambda: beep(client))
    top_blue = ttk.Button(frame, text='Top Blue', command=lambda: speak(client))
    play_song = ttk.Button(frame, text='Play a Song', command=lambda: play(client))

    speed_entry_box.grid()
    go_forward_button.grid()
    top_red.grid()
    top_blue.grid()
    play_song.grid()

    go_forward_button['command'] = \
        lambda: handle_go_forward(speed_entry_box, client)


def handle_go_forward(box, client):
    """
    Tells the robot to go forward at the speed specified in the given entry box.
    """
    speed = box.get()
    client.send_message('go', [speed])

def beep(client):
    client.send_message('button_pressed', ['top-red'])

def speak(client):
    client.send_message('button_pressed', ['top-blue'])

def play(client):
    client.send_message('play_song')


main()

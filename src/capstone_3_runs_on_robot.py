"""
Mini-application:  Buttons on a Tkinter GUI tell the robot to:
  - Go forward at the speed given in an entry box.

Also: responds to Beacon button-presses by beeping, speaking.

This module runs on the ROBOT.
It uses MQTT to RECEIVE information from a program running on the LAPTOP.

Authors:  David Mutchler, his colleagues, and Rui Fang.
"""

import rosebotics_even_newer as rb
import time
import mqtt_remote_method_calls as com
import ev3dev.ev3 as ev3


class MyDelegate(object):

    def __init__(self):
        self.robot = rb.Snatch3rRobot()
        self.mqtt_client = None
        self.ev3 = ev3

    def go(self, speed):
        self.robot.drive_system.start_moving(int(speed), int(speed))
        time.sleep(5)
        self.robot.drive_system.stop_moving()

    def button_pressed(self, button):
        if button == 'top-red':
            ev3.Sound.beep()

        if button == 'top-blue':
            ev3.Sound.speak('Hello. How are you?')

    def play_song(self):
        ev3.Sound.tone([
            (392, 350, 100), (392, 350, 100), (392, 350, 100), (311.1, 250, 100),
            (466.2, 25, 100), (392, 350, 100), (311.1, 250, 100), (466.2, 25, 100),
            (392, 700, 100), (587.32, 350, 100), (587.32, 350, 100),
            (587.32, 350, 100), (622.26, 250, 100), (466.2, 25, 100),
            (369.99, 350, 100), (311.1, 250, 100), (466.2, 25, 100), (392, 700, 100),
            (784, 350, 100), (392, 250, 100), (392, 25, 100), (784, 350, 100),
            (739.98, 250, 100), (698.46, 25, 100), (659.26, 25, 100),
            (622.26, 25, 100), (659.26, 50, 400), (415.3, 25, 200), (554.36, 350, 100),
            (523.25, 250, 100), (493.88, 25, 100), (466.16, 25, 100), (440, 25, 100),
            (466.16, 50, 400), (311.13, 25, 200), (369.99, 350, 100),
            (311.13, 250, 100), (392, 25, 100), (466.16, 350, 100), (392, 250, 100),
            (466.16, 25, 100), (587.32, 700, 100), (784, 350, 100), (392, 250, 100),
            (392, 25, 100), (784, 350, 100), (739.98, 250, 100), (698.46, 25, 100),
            (659.26, 25, 100), (622.26, 25, 100), (659.26, 50, 400), (415.3, 25, 200),
            (554.36, 350, 100), (523.25, 250, 100), (493.88, 25, 100),
            (466.16, 25, 100), (440, 25, 100), (466.16, 50, 400), (311.13, 25, 200),
            (392, 350, 100), (311.13, 250, 100), (466.16, 25, 100),
            (392.00, 300, 150), (311.13, 250, 100), (466.16, 25, 100), (392, 700)
        ]).wait()



def main():
    robot_action = MyDelegate()
    mqtt_client = com.MqttClient(robot_action)
    robot_action.mqtt_client = mqtt_client
    mqtt_client.connect('robo32', 'fr')
    mqtt_client.send_message('Connected!')
    robot = rb.Snatch3rRobot()
    while True:
        if robot.beacon_button_sensor.is_top_red_button_pressed() is True:
            ev3.Sound.beep().wait()

        if robot.beacon_button_sensor.is_top_blue_button_pressed() is True:
            ev3.Sound.speak("Hello. How are you?").wait()
        time.sleep(0.01)


main()
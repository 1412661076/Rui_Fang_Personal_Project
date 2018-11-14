"""
  Capstone Personal Project.  Code written by Rui Fang.
  Fall term, 2018-2019.
"""

import mqtt_remote_method_calls as com
import time
import ev3dev.ev3 as ev3
import rosebotics_even_newer as rb


class MyDelegate(object):
    def __init__(self):
        self.robot = rb.Snatch3rRobot()
        self.mqtt_client = None
        self.ev3 = ev3

    def go_straight(self, dist):
        self.robot.drive_system.go_straight_inches(int(dist)/6)
        if self.robot.proximity_sensor.get_distance_to_nearest_object_in_inches() < 20:
            self.robot.drive_system.go_straight_inches(-5)
        if self.robot.camera.get_biggest_blob().get_area() >= 500:
            self.robot.drive_system.go_straight_inches(-5)
        if self.robot.color_sensor.get_color()==6:
            self.dig()

    def turn_angle(self, degree):
        self.robot.drive_system.spin_in_place_degrees(int(degree))

    def find_beacon(self):
        while True:
            self.robot.drive_system.spin_in_place_degrees(3)
            angle = self.robot.beacon_sensor.get_heading_to_beacon()
            if angle <= 3 and angle >= -3:
                while True:
                    self.robot.drive_system.start_moving()
                    if self.robot.beacon_sensor.get_distance_to_beacon() <= 10:
                        break
            break

    def beep_once(self):
        self.ev3.Sound.beep()
        ev3.Sound.beep()

    def beep_twice(self):
        self.ev3.Sound.beep().wait()
        time.sleep(0.15)
        self.ev3.Sound.beep().wait()

    def dig(self):
        self.calibrate()
        self.ev3.Sound.tone([
            (392, 350, 100), (392, 350, 100), (392, 350, 100), (311.1, 250, 100),
            (466.2, 25, 100), (392, 350, 100), (311.1, 250, 100), (466.2, 25, 100),
            (392, 700, 100), (587.32, 350, 100), (587.32, 350, 100),
            (587.32, 350, 100), (622.26, 250, 100), (466.2, 25, 100),
            (369.99, 350, 100), (311.1, 250, 100), (466.2, 25, 100), (392, 700, 100)
        ]).wait()

    def play_note(self, pitch):
        self.ev3.Sound.tone(int(pitch), 350)

    def get_coin(self):
        self.beep_twice()

    def get_trapped(self):
        self.robot.drive_system.turn_degrees(360)
        self.robot.drive_system.turn_degrees(360)

    def you_win(self):
        self.ev3.Sound.play('/home/robot/csse120/frtachi/src/Ta_Da.wav').wait()
        self.ev3.Sound.speak('You win').wait()

    def you_lose(self):
        self.ev3.Sound.play('/home/robot/csse120/frtachi/src/lose.wav').wait()
        self.ev3.Sound.speak('You lose').wait()

    def calibrate(self):
        self.robot.arm.calibrate()


def main():
    robot_action = MyDelegate()
    mqtt_client = com.MqttClient(robot_action)
    robot_action.mqtt_client = mqtt_client
    mqtt_client.connect('robo32', 'fr')

    while True:
        time.sleep(0.01)
        if input() == 'p':
            break


main()

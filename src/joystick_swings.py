#!/usr/bin/env python
import rospy
from swings import Swings
from sensor_msgs.msg import Joy

class JoystickSwings():
    def __init__(self):
        self.swing = Swings()
        self.sub = rospy.Subscriber("joy", Joy, self.callback)
        self.buttons = {
                'up': 4,
                'down': 6,
                'deadman': 10,
                'swing': 15,
                'punch': 13
                }
        isHit = lambda x: x > 0
        self.getHits = lambda buttons_presses: [isHit(x) for x in buttons_presses]
        self.button_states = None
        self.detect = lambda (curr, prev): [ not p and c for(c,p) in zip(curr, prev)]
        rospy.spin()
        self.button_states = [0]*17

    def command(self, cmds):
        if cmds[self.buttons['up']]:
            self.swing.up()

        if cmds[self.buttons['down']]:
            self.swing.down()

        if cmds[self.buttons['swing']]:
            self.swing.swing()

        if cmds[self.buttons['punch']]:
            self.swing.punch()
        

    def callback(self, data):
        button_states = self.getHits(data.buttons)
        if sum(button_states) > 0:
            if button_states[self.buttons['deadman']]:
                button_toggles = self.detect((button_states, self.button_states))
                if sum(button_toggles) > 0:
                    if button_toggles[self.buttons['swing']]:
                        self.swing.swing()
                    elif button_toggles[self.buttons['punch']]:
                        self.swing.punch()
                if button_states[self.buttons['up']]:
                    self.swing.up()
                elif button_states[self.buttons['down']]:
                    self.swing.down()

            self.button_states = button_states

        else:
            self.button_states = [0]*len(button_states)

if __name__=="__main__":
    rospy.init_node("joystick_swings")
    JoystickSwings()

        


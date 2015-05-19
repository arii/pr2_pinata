#!/usr/bin/env python
import rospy
from swings import Swings
from std_srvs.srv import Empty

class SwingsServer():
    def __init__(self):
        rospy.init_node("swings_server")
        self.swing = Swings()

        rospy.Service("pinata_punch", Empty, self.punch)
        rospy.Service("pinata_swing", Empty, self.swing)
        rospy.Service("pinata_up", Empty, self.up)
        rospy.Service("pinata_down", Empty, self.down)
        rospy.loginfo("swing server loaded")
        rospy.spin()

    def punch(self, req):
        self.swing.punch()
        return []

    def swing(self, req):
        self.swing.swing()
        return []

    def up(self, req):
        self.swing.up()
        return []

    def down(self, req):
        self.swing.down()
        return []


if __name__== "__main__":
    server = SwingsServer()




    
    



import roslib
roslib.load_manifest("pr2_awesomeness")
import rospy
import actionlib
from awesome_arm_controller import ArmController


class Swings():
    def __init__(self):
        
        self.ctrl = ArmController(event_detector=True)
        self.arm = "r"

        self.poses = {
                'home':[-1.63, -0.17, -1.57, -2.06, 6.37, -1.3, 12.31],
                'punch':[-0.31, -0.19, -1.6, -2.12, 6.41, -0.26, 12.43],
                'swing':[-1.57, -0.13, -1.58, -0.38, 6.5, -0.09, 12.12],
                'release':[-0.31, -0.15, -1.67, -0.15, 6.44, -0.19, 12.37]
                }
        self.move('home', 0) 
        self.Z_INC = .05
        self.ctrl.close_gripper(self.arm)

    def move(self, name, move_duration=3.0, blocking=True):
        curr_z = self.ctrl.get_joint_angles()[self.arm][1]
        new_pose = self.poses[name]
        new_pose[1] =  curr_z
        self.ctrl.joint_movearm(self.arm, new_pose, move_duration)
    
    def hit(self, hit_type):
        self.move(hit_type)
        self.move('release', move_duration=.8)
        self.move('home', blocking=False)
    
    def move_shoulder (self, up=True):
        curr = self.ctrl.get_joint_angles()[self.arm]
        inc = curr[1] + self.Z_INC*(-1 if up else 1)
        curr[1] = inc
        self.ctrl.joint_movearm(self.arm, curr, 1, blocking=False)

    # public functions

    def punch(self):
        self.hit('punch')

    def swing(self):
        self.hit('swing')

    def up(self):
        self.move_shoulder(up=True)

    def down(self):
        self.move_shoulder(up=False)




if __name__== "__main__":
    rospy.init_node("pinata_swings")
    swing = Swings()
    c = 0
    while c != "q":
        c = raw_input("p to punch, s to swing, u up, d down, q to quit")
        if c == "p":
            swing.punch()
        elif c == "s":
            swing.swing()
        elif c == "u":
            swing.up()
        elif c == "d":
            swing.down()




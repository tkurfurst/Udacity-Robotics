# --------------
# User Instructions
# 
# Define a function cte in the robot class that will
# compute the crosstrack error for a robot on a
# racetrack with a shape as described in the video.
#
# You will need to base your error calculation on
# the robot's location on the track. Remember that 
# the robot will be traveling to the right on the
# upper straight segment and to the left on the lower
# straight segment.
#
# --------------
# Grading Notes
#
# We will be testing your cte function directly by
# calling it with different robot locations and making
# sure that it returns the correct crosstrack error.  
 
from math import *
import random


# ------------------------------------------------
# 
# this is the robot class
#

class robot:

    # --------
    # init: 
    #    creates robot and initializes location/orientation to 0, 0, 0
    #

    def __init__(self, length = 20.0):
        self.x = 0.0
        self.y = 0.0
        self.orientation = 0.0
        self.length = length
        self.steering_noise = 0.0
        self.distance_noise = 0.0
        self.steering_drift = 0.0

    # --------
    # set: 
    #	sets a robot coordinate
    #

    def set(self, new_x, new_y, new_orientation):

        self.x = float(new_x)
        self.y = float(new_y)
        self.orientation = float(new_orientation) % (2.0 * pi)


    # --------
    # set_noise: 
    #	sets the noise parameters
    #

    def set_noise(self, new_s_noise, new_d_noise):
        # makes it possible to change the noise parameters
        # this is often useful in particle filters
        self.steering_noise = float(new_s_noise)
        self.distance_noise = float(new_d_noise)

    # --------
    # set_steering_drift: 
    #	sets the systematical steering drift parameter
    #

    def set_steering_drift(self, drift):
        self.steering_drift = drift
        
    # --------
    # move: 
    #    steering = front wheel steering angle, limited by max_steering_angle
    #    distance = total distance driven, most be non-negative

    def move(self, steering, distance, 
             tolerance = 0.001, max_steering_angle = pi / 4.0):

        if steering > max_steering_angle:
            steering = max_steering_angle
        if steering < -max_steering_angle:
            steering = -max_steering_angle
        if distance < 0.0:
            distance = 0.0


        # make a new copy
        res = robot()
        res.length         = self.length
        res.steering_noise = self.steering_noise
        res.distance_noise = self.distance_noise
        res.steering_drift = self.steering_drift

        # apply noise
        steering2 = random.gauss(steering, self.steering_noise)
        distance2 = random.gauss(distance, self.distance_noise)

        # apply steering drift
        steering2 += self.steering_drift

        # Execute motion
        turn = tan(steering2) * distance2 / res.length

        if abs(turn) < tolerance:

            # approximate by straight line motion

            res.x = self.x + (distance2 * cos(self.orientation))
            res.y = self.y + (distance2 * sin(self.orientation))
            res.orientation = (self.orientation + turn) % (2.0 * pi)

        else:

            # approximate bicycle model for motion

            radius = distance2 / turn
            cx = self.x - (sin(self.orientation) * radius)
            cy = self.y + (cos(self.orientation) * radius)
            res.orientation = (self.orientation + turn) % (2.0 * pi)
            res.x = cx + (sin(res.orientation) * radius)
            res.y = cy - (cos(res.orientation) * radius)

        return res




    def __repr__(self):
        return '[x=%.5f y=%.5f orient=%.5f]'  % (self.x, self.y, self.orientation)


############## ONLY ADD / MODIFY CODE BELOW THIS LINE ####################
   
    def cte(self, radius):
       
        def ang(x,y, radius):
            if y > radius:
                num = y - radius
            else:
                num = radius - y
            if x <= radius:
                den = radius - x
            elif x > 3. * radius:
                den = x - 3. * radius
            #
            # check signs - should be positive in cases II and V - negtive in cases I amd VI
            # here ALWAYS posutive
            #
            return atan(num/den)


        r = radius

        # robot on left circle (L)
        if self.x <= r:
            theta = ang(self.x, self.y, r)
            # case I: robot on upper half
            # desired (x, y) = (x*, y*)
            if self.y >= r:
                x = r - r * cos(theta)
                y = r + r * sin(theta)
                cte = sqrt((y - self.y)**2 + (x - self.x)**2)
                if self.x > x and self.y < y:
                    cte = -cte
            # case II: robot on lower half
            # desired (x, y) = (x*, y*)
            else:    
                x = r - r * cos(theta)
                y = r - r * sin(theta)
                cte = sqrt((y - self.y)**2 + (x - self.x)**2)
                if self.x > x and self.y > y:
                    cte = -cte
        # robot on straight (S)
        elif self.x > r and self.x <= (3. * r):    
            # case III: robot on upper half
            # desired y = 2r
            if self.y > r:
                y = 2. * r
                cte = self.y - y
            # case IV: robot on lower half
            # desired y = 0
            else:
                y = 0.
                cte = y - self.y
        # robot on right circle (R)
        elif self.x > (3. * r):
            theta = ang(self.x, self.y, r)
            # case V: robot on upper half
            # desired (x, y) = (x*, y*)
            if self.y >= r:
                x = 3. * r + r * cos(theta)
                y = r + r * sin(theta)
                cte = sqrt((y - self.y)**2 + (x - self.x)**2)
                if self.x < x and self.y < y:
                    cte = -cte
            # case VI: robot on lower half
            # desired (x, y) = (x*, y*)
            else:    
                x = 3. * r + r * cos(theta)
                y = r - r * sin(theta)
                cte = sqrt((y - self.y)**2 + (x - self.x)**2)
                if self.x < x and self.y > y:
                    cte = -cte
        return cte
    
############## ONLY ADD / MODIFY CODE ABOVE THIS LINE ####################




# ------------------------------------------------------------------------
#
# run - does a single control run.

# added plotting capabilities
import matplotlib.pyplot as plt

def run(params, radius, printflag = False):
    myrobot = robot()
    # start at top middle
    # myrobot.set(2. * radius, 2.0 * radius, 0.)
    # start at left middle
    myrobot.set(0.0, radius, pi / 2.0)
    speed = 1.0 # motion distance is equal to speed (we assume time = 1)
    err = 0.0
    int_crosstrack_error = 0.0
    N = 129 # was 200
    cte = []
    crosstrack_error = myrobot.cte(radius) # You need to define the cte function!

    for i in range(N*2):
        diff_crosstrack_error = - crosstrack_error
        crosstrack_error = myrobot.cte(radius)
        cte.append(crosstrack_error)
        diff_crosstrack_error += crosstrack_error
        int_crosstrack_error += crosstrack_error
        steer = - params[0] * crosstrack_error \
                - params[1] * diff_crosstrack_error \
                - params[2] * int_crosstrack_error
        myrobot = myrobot.move(steer, speed)
        if i >= 0: # was N
            err += crosstrack_error ** 2
        if printflag:
            print i, myrobot, "CTE= %2.2f steer= %4.4f" %(crosstrack_error, steer), err/float(N)
            # added plotting capabilities
            if i < N:
                plt.scatter(myrobot.x, myrobot.y, color='red')
            else:
                plt.scatter(myrobot.x, myrobot.y, color='blue')
    plt.figure()
    plt.plot(cte)

    return err / float(N)

radius = 25.0
params = [10.0, 15.0, 0.0]
err = run(params, radius, True)
print '\nFinal parameters: ', params, '\n ->', err

# added plotting capabilities
plt.show()


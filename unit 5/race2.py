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
import numpy
import matplotlib.pyplot
#from turtle import *



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
        # 
        #
        # Add code here
        #
        #            
        
        # Three distinct possibilities for relative cte calculation:
        # (1) Left most half circle
        # (2) Straights
        # (3) Right most half circle
        # 
        # x == [0, 4r], y == [] if (1), [] if (2), [] if 3
        #
        # define cte to +ve if car outside track, -ve if inside track???

        def ang(x,y, radius):
            if y > radius:
                num = y - radius
            else:
                num = radius - y
            if x <= radius:
                den = radius - x
            elif x > 3. * radius:
                den = x - 3. * radius
            return atan(num/den)

        r = radius


        if self.x <= r:
            # targeting left circle
            """
            theta = ang(self.x, self.y, r)
            x = r + r * cos(theta)
            y = r + r * sin(theta)
            #print 'x < r:', theta, x, y
            cte = self.y - y
            #cte = sqrt((self.x - x)**2 + (self.y - y)**2) 
            # was if < y
            if self.y < y:
                cte = -cte
            """
            cte = sqrt((self.x - r)**2 + (self.y - r)**2) - r
        elif self.x > r and self.x <= (3. * r):
            # targeting straight
            """
            x = self.x
            if self.y > r:
                y = 2. * r
            else:
                y = 0.
            cte = self.y - y
            #cte =  sqrt((self.x - x)**2 + (self.y - y)**2)
            if self.y >= r and self.y <= (2. * r):
                cte = cte
            elif self.y <= r:
                cte = -cte 
            """
            if self.y > r:
                cte = self.y - 2 * r
            else:
                cte = -self.y    

        elif self.x > (3. * r):
            # targeting right circle
            """
            theta = ang(self.x, self.y, r)
            x = 3 * r + r * cos(theta)
            y = r + r * sin(theta)
            #print 'x > 3r:', theta, x, y
            cte = self.y - y
            #cte = sqrt((self.x - x)**2 + (self.y - y)**2) 
            # was if < y
            if self.y < y:
                cte = -cte
            """
            cte = sqrt((self.x - 3 * r)**2 + (self.y - r)**2) - r
        return cte
    
############## ONLY ADD / MODIFY CODE ABOVE THIS LINE ####################




# ------------------------------------------------------------------------
#
# run - does a single control run.


def run(params, radius, printflag = False):
    myrobot = robot()
    myrobot.set(0.0, radius, pi / 2.0)
    speed = 1.0 # motion distance is equal to speed (we assume time = 1)
    err = 0.0
    int_crosstrack_error = 0.0
    N = 200

    # REMOVE
    res = [[myrobot.x, myrobot.y]]
    # REMOVE
    if printflag:
        print myrobot
    
    crosstrack_error = myrobot.cte(radius) # You need to define the cte function!

    for i in range(N*2):
        diff_crosstrack_error = - crosstrack_error
        crosstrack_error = myrobot.cte(radius)
        diff_crosstrack_error += crosstrack_error
        int_crosstrack_error += crosstrack_error
        steer = - params[0] * crosstrack_error \
                - params[1] * diff_crosstrack_error \
                - params[2] * int_crosstrack_error
        myrobot = myrobot.move(steer, speed)

        # REMOVE
        res.append([myrobot.x, myrobot.y])
        # REMOVE

        if i >= N:
            err += crosstrack_error ** 2
        if printflag:
            print myrobot

        return err / float(N)

    matplotlib.pyplot.plot([x[0] for x in res], [x[1] for x in res])
    matplotlib.pyplot.show()

    """
    import matplotlib.pyplot as mtpl
    mtpl.figure()
    mtpl.hold(True)
    mtpl.plot([p[0] for p in res], [p[1] for p in res], label='Car path')
    mtpl.legend()
    mtpl.show()
    """

radius = 25.0
params = [10.0, 15.0, 0]
#params = [10.8, 15.5, 0.95]
err = run(params, radius, True)
print '\nFinal paramaeters: ', params, '\n ->', err


"""
def run(params, radius, printflag = False, turtle = False):
    myrobot = robot()
    myrobot.set(0.0, radius, pi / 2.0)
    speed = 1.0 # motion distance is equal to speed (we assume time = 1)
    err = 0.0
    int_crosstrack_error = 0.0
    N = 200

    if True:        
        # draw track
        penup()
        color('red', 'yellow')        
        setx(radius)
        sety(0)
        setheading(-180)
        pendown()
        begin_fill()
        circle(-radius, extent=180)
        forward(2*radius)
        circle(-radius, extent=180)
        forward(2*radius)
        end_fill()

        # robot starting position
        penup()
        setx(myrobot.x)
        sety(myrobot.y)
        setheading(myrobot.orientation*(180/pi))
        color("blue")
        pendown()

    crosstrack_error = myrobot.cte(radius) # You need to define the cte function!

    for i in range(N*2):
        diff_crosstrack_error = - crosstrack_error
        crosstrack_error = myrobot.cte(radius)
        diff_crosstrack_error += crosstrack_error
        int_crosstrack_error += crosstrack_error
        steer = - params[0] * crosstrack_error \
                - params[1] * diff_crosstrack_error \
                - params[2] * int_crosstrack_error
        myrobot = myrobot.move(steer, speed)
        if i >= N:
            err += crosstrack_error ** 2
        if printflag:
            print (myrobot)
        if turtle:        
            setx(myrobot.x)
            sety(myrobot.y)
            setheading(myrobot.orientation * (180/pi))
    return err / float(N)

radius = 25.0
params = [10.0, 15.0, 0]
err = run(params, radius, True, True)
print ('\nFinal paramaeters: ', params, '\n ->', err)
"""    


"""
def twiddle(tol = 0.002): # 0.00001 - Make this tolerance bigger if you are timing out!
############## ADD CODE BELOW ####################
    
    # -------------
    # Add code here
    # -------------

    nparams = 3

    p = [0. for entry in range(nparams)]
    dp = [1. for entry in range(nparams)]

    n=0
    best_error = run(p, 25.0)  
    
    while(sum(dp) > tol):
        for i in range(len(p)):
            p[i] += dp[i]
            error = run(p, 25.0)
            # if +dp improves, increase the size of dp
            if error < best_error:
                best_error = error
                dp[i] *= 1.1
            # otherwise, try -dp
            else:
                p[i] -= 2 * dp[i]
                error = run(p, 25.0)
                # if - dp improves, increase the size of dp
                if error < best_error:
                    best_error = error
                    dp[i] *= 1.1
                else:
                    # neither +dp nor -dp works, decrease the size of dp
                    p[i] += dp[i]
                    dp[i] *= 0.9
        n += 1

        print 'Twiddle #:', n, p, ' --> ', best_error
    
    return run(p, 25.0)

twiddle()
"""


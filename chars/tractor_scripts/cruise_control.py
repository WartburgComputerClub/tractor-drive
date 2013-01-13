# file: cruise_control.py
# author: Andrew Reisner <andrew.reisner@gmail.com>
# This class provides a simple PID cruise control

import time

class CruiseControl:
    
    def __init__(self,obj,settings):
        self.prev = time.time()
        self.integral = 0
        self.prevError = 0
        
        self.closeCount = 0
        
        # eventually going in settings file
        self.kp = settings.CRUISE_CONTROL['kp']
        self.ki = settings.CRUISE_CONTROL['ki']
        self.kd = settings.CRUISE_CONTROL['kd']
        self.SP = settings.CRUISE_CONTROL['SP']
        self.obj = obj
        self.power = 0
        
    def reset(self):
        self.prev = time.time()
        self.integral = 0
        self.prevError = 0
        self.power = 0
        
    def update(self):
        car = self.obj
        trac = self.obj['handle']
        speed = car.getLinearVelocity().magnitude
        dt = time.time() - self.prev
        error = self.SP - speed
        self.integral = self.integral + (error * dt)
        self.derivative = (error - self.prevError) / dt
        self.power = (self.kp*error) + (self.ki*self.integral) + (self.kd*self.derivative)
        self.prevError = error
        self.prev = dt + self.prev
        
        if trac.simFlag:
            trac.simFile.write('{} {}\n'.format(self.prev,speed))
            if abs(error) < .1:
                self.closeCount += 1
            else:
                self.closeCount = 0
            if self.closeCount > 9:
                trac.simOver = True
            print(self.power)
        
    def getPower(self):
        max_power = 100   # eventually going in settings file
        if (abs(self.power) > max_power):
            if self.power > 0:
                return max_power
            else:
                return -1 * max_power
        else:
            return self.power
    

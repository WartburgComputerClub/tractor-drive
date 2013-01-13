import serial

class Wheel:
    
    def __init__(self,settings):
        self.settings = settings
        try:
            self.ser = serial.Serial(settings.WHEEL, dsrdtr=False)
            self.ser.setDTR(False)
            #self.setPower(10)
            self.WHEEL_CONNECTED = True
        except:
            self.WHEEL_CONNECTED = False
            
        self.steer = 0
        self.right_max = settings.CALIBRATION['right_max']
        self.left_max = settings.CALIBRATION['left_max']
        self.midpoint = settings.CALIBRATION['midpoint']
            
    def update(self):
        if not self.WHEEL_CONNECTED:
            return
        ser = self.ser
        x = 0
        if (ser.inWaiting() > 100):
            ser.flushInput()
        if (ser.inWaiting()):
            try:
                x = eval(ser.readline()[0:-2])
            except: 
                return
        else:
            return 
        scale = 1
        
        x -= self.midpoint
        if x > 0:
            x *= (scale/(max(self.left_max,self.right_max) - self.midpoint))
        else:
            x *= (scale/(self.midpoint - min(self.left_max,self.right_max)))
            
        if self.left_max < self.right_max:
            x *= -1
            
        x = round(x,2)
        turn = x
        print('turn:',x)
        self.steer = turn
        
    def getSteer(self):
        return self.steer
    
    def connected(self):
        return self.WHEEL_CONNECTED
            

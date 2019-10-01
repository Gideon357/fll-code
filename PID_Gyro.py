from ev3dev2.sensor.lego import GyroSensor
from ev3dev2.motor import Motor, LargeMotor, MoveTank
gyro = GyroSensor()
motor = Motor()
gyro.mode = GYRO-ANG

def gyroPID(ki,kp,kd,target,wheel,speed,distance)
    subprocesses.call("echo reset > $MC/command")
    counts = motor.count_per_rot
    r = distance/wheel
    m = r*counts
    while True:
        error = target - gyro.mode
        integral = integral + error
        error - last_error = derivative
        integralResult = integral*ki
        porportionResult = kp*error
        derivResult = kd*derivative
        result = integralResult+derivResult+porportionResult
        tank.on(result)
        error = lastError
        if motor.position => m:
            return False
        else:
            return True

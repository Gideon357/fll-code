from ev3dev2.sensor.lego import GyroSensor
gyro = GyroSensor()
gyro.mode = GYRO-ANG

def gyroPID(ki,kp,kd,target,wheel,speed,distance)
    while True:
        error = target - gyro.mode
        integral = integral + error
        error - last_error = derivative
        integralResult = integral*ki
        porportionResult = kp*error
        derivResult = kd*derivative
        result = integralResult+derivResult+porportionResult
        tank_drive = MoveTank(OUTPUT_A, OUTPUT_B)
        r = wheel/distance
        tank.on(result)
        error = lastError
""" TODO: Incorprate move block into correction to allow this to run while moving forward.
Add to Griffy Class."""
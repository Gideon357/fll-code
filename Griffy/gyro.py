def on_for_distance(self, speed, distance_in, brake=True, block=True, use_gyro=True, kp=0.1, ki=0.1, kd=0.1, target=0):
    """
    Drives for a certain distance
    and has a toglable gyro feature
    TODO: Define Parameters so people know what they are for
    TODO: Explain gyro algorithm
    """
    distance_mm = self.in_to_mm(distance_in)
    if use_gyro:
        gyro = self.left_gyro_sensor
        gyro.reset()
        integral = 0.0
        last_error = 0.0
        derivative = 0.0
        # rotations = distance_mm / self.wheel_circumference
        # degrees = 360 * rotations
        self.reset(self.right_large_motor)
        self.reset(self.left_large_motor)
        speed_native_units = speed.to_native_units(self.left_large_motor)
        while True:
            error = target - gyro.angle
            integral = integral + error
            derivative = error - last_error
            last_error = error
            turn_native_units = (kp * error) + (ki * integral) + (kd * derivative)
            left_speed = speed_native_units(SpeedNativeUnits - turn_native_units)
            right_speed = speed_native_units(SpeedNativeUnits + turn_native_units)
            self.sleep_in_loop()
            self.on(left_speed, right_speed)
    else:
        super().on_for_distance(speed, distance_mm, brake, block)

# def move(ki=0, kp=0, kd=0, target=0, drive_with_gyro=True):
#     """ Moves the robot a specified amount of inches. Uses PID algorithim and the Gyro Sensor to correct drift"""
#     if drive_with_gyro == True:
#                 error = target - gyro.mode
#                 integral = integral + error
#                 derivative = error - last_error
#                 last error = error
#                 turn_native_units = (kp * error) + (ki * integral) + (kd * derivative)
#                 if motor.position => m:
#                     return False #If the motor has moved the correct amount, it ends the loop
#                 else:
#                     return True
#         except: # If tacho motor does not initialize, it runs without gyro
#             tank.on_for_rotations(LeftSpeed,RightSpeed,r)
#             try:
#                 console.text_at('An Exception Occured, Ran Without Gyro. Check Motor and Drivers', column=1, row=5, reset_console=True, inverse=True)
#             except:
#                 pass
#         else:
#             tank.on_for_rotations(LeftSpeed,RightSpeed,r)

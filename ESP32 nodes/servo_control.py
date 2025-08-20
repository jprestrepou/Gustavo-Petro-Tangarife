# servo_control.py

from machine import Pin, PWM
import time

class Servo:
    def __init__(self, pin):
        self.pwm = PWM(Pin(pin), freq=50)

    def set_angle(self, angle):  # angle entre 0 y 180
        duty = int(40 + (angle / 180) * 80)  # Ajuste típico de 40–115
        self.pwm.duty(duty)
        time.sleep_ms(500)

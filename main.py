from umqtt.simple import MQTTClient
import network
import time
import config
from motor_control import Motor
from led_control import LED
from servo_control import Servo
from utils import ejecutar_comando

# Conexión WiFi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect('NOMBRE_WIFI', 'CONTRASEÑA_WIFI')
while not wifi.isconnected():
    time.sleep(0.5)
print("Conectado a WiFi:", wifi.ifconfig())

# Inicialización de actuadores
actuadores = {
    "motor1": Motor(config.M1_IN1, config.M1_IN2, config.M1_PWM),
    "motor2": Motor(config.M2_IN1, config.M2_IN2, config.M2_PWM),
    "motor3": Motor(config.M3_IN1, config.M3_IN2, config.M3_PWM),
    "motor4": Motor(config.M4_IN1, config.M4_IN2, config.M4_PWM),
    "led": LED(config.LED_PIN),
    "servo": Servo(config.SERVO_PIN)
}

# Callback cuando llega un mensaje
def callback_mqtt(topic, msg):
    comando = msg.decode('utf-8')
    print(f"Comando recibido: {comando}")
    ejecutar_comando(comando, actuadores)

# Conexión al broker MQTT (el ROS publica aquí)
client = MQTTClient("esp32_robot", "192.168.1.100")  # IP del broker (nodo ROS)
client.set_callback(callback_mqtt)
client.connect()
client.subscribe(b"robot/comandos")
print("Suscrito a robot/comandos")

# Bucle principal
while True:
    client.check_msg()
    time.sleep(0.1)

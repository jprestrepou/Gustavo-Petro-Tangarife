from machine import Pin
import network
import time
from umqtt.simple import MQTTClient

# Pines de control del puente H
in1 = Pin(5, Pin.OUT)
in2 = Pin(18, Pin.OUT)
in3 = Pin(19, Pin.OUT)
in4 = Pin(21, Pin.OUT)

# ========================
# CONFIGURA TUS CREDENCIALES
SSID = 'MARTA LUCIA'
PASSWORD = '43665830'
BROKER = '192.168.1.10'  # IP de la Raspberry Pi
# ========================

def conectar_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Conectando a red WiFi...')
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            time.sleep(0.5)
    print('Conectado a WiFi:', wlan.ifconfig())

def detener():
    in1.value(0)
    in2.value(0)
    in3.value(0)
    in4.value(0)

def adelante():
    in1.value(1)
    in2.value(0)
    in3.value(1)
    in4.value(0)

def atras():
    in1.value(0)
    in2.value(1)
    in3.value(0)
    in4.value(1)

def izquierda():
    in1.value(0)
    in2.value(1)
    in3.value(1)
    in4.value(0)

def derecha():
    in1.value(1)
    in2.value(0)
    in3.value(0)
    in4.value(1)

def recibir_mensaje(topic, msg):
    comando = msg.decode('utf-8')
    print('Comando recibido:', comando)
    if comando == 'adelante':
        print("ros2 topic adelante")
        adelante()
    elif comando == 'atras':
        atras()
    elif comando == 'izquierda':
        izquierda()
    elif comando == 'derecha':
        derecha()
    else:
        detener()

# Conectar a WiFi
conectar_wifi(SSID, PASSWORD)

# Conectar a MQTT y suscribirse
cliente = MQTTClient("esp32_motor_node", BROKER)
cliente.set_callback(recibir_mensaje)
cliente.connect()
cliente.subscribe(b"robot/motor")
print("Conectado al broker MQTT y suscrito a robot/motor")

try:
    while True:
        cliente.wait_msg()
except KeyboardInterrupt:
    print("Interrumpido por el usuario")
    detener()
    cliente.disconnect()

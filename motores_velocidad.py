import network
import time
from machine import Pin, PWM
from umqtt.simple import MQTTClient

# --- CONFIGURACIÓN WiFi ---
WIFI_SSID = "MARTA LUCIA"
WIFI_PASS = "43665830"

# --- CONFIGURACIÓN MQTT ---
MQTT_BROKER = "192.168.1.10"  # por ejemplo: "192.168.1.100"
MQTT_CLIENT_ID = "esp32_motor"
MQTT_TOPIC_DIR = b"robot/motor"
MQTT_TOPIC_VEL = b"robot/velocidad"

# --- PINES MOTORES (ajusta según conexión física) ---
# Motor A
in1 = Pin(14, Pin.OUT)
in2 = Pin(27, Pin.OUT)
# Motor B
in3 = Pin(26, Pin.OUT)
in4 = Pin(25, Pin.OUT)

# PWM para velocidad
pwmA = PWM(Pin(12), freq=1000)
pwmB = PWM(Pin(33), freq=1000)
velocidad = 500  # valor inicial (0 a 1023)

# --- Conexión WiFi ---
def conectar_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Conectando a WiFi...')
        wlan.connect(WIFI_SSID, WIFI_PASS)
        while not wlan.isconnected():
            pass
    print('Conectado a WiFi:', wlan.ifconfig())

# --- Callback MQTT ---
def callback(topic, msg):
    global velocidad
    print('Mensaje recibido:', topic, msg)

    if topic == MQTT_TOPIC_DIR:
        comando = msg.decode('utf-8')
        print(comando)
        if comando == "adelante":
            in1.value(1)
            in2.value(0)
            in3.value(1)
            in4.value(0)
        elif comando == "atras":
            in1.value(0)
            in2.value(1)
            in3.value(0)
            in4.value(1)
        elif comando == "izquierda":
            in1.value(0)
            in2.value(1)
            in3.value(1)
            in4.value(0)
        elif comando == "derecha":
            in1.value(1)
            in2.value(0)
            in3.value(0)
            in4.value(1)
        elif comando == "detener":
            in1.value(0)
            in2.value(0)
            in3.value(0)
            in4.value(0)
    elif topic == MQTT_TOPIC_VEL:
        try:
            velocidad = int(msg)
            velocidad = max(0, min(1023, velocidad))  # Limita entre 0 y 1023
            pwmA.duty(velocidad)
            pwmB.duty(velocidad)
            print("Velocidad actual:", velocidad)
        except:
            print("Error al convertir velocidad")

# --- Main ---
conectar_wifi()
cliente = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER)
cliente.set_callback(callback)
cliente.connect()
cliente.subscribe(MQTT_TOPIC_DIR)
cliente.subscribe(MQTT_TOPIC_VEL)
print("Conectado a broker MQTT y suscrito a topics")

# Iniciar con velocidad inicial
pwmA.duty(velocidad)
pwmB.duty(velocidad)

# Loop principal
try:
    while True:
        cliente.check_msg()
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Finalizando...")
    cliente.disconnect()

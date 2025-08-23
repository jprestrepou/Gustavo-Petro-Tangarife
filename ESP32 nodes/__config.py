# --- Configuración WiFi ---
WIFI_SSID = "TuSSID"
WIFI_PASS = "TuPassword"
IP_FIJA   = "192.168.1.123"
MASK      = "255.255.255.0"
GATEWAY   = "192.168.1.1"
DNS       = "8.8.8.8"

# --- Configuración MQTT ---
MQTT_BROKER    = "192.168.1.150"
MQTT_CLIENT_ID = "esp32_motores"
MQTT_TOPIC_DIR = b"robot/direccion"
MQTT_TOPIC_VEL = b"robot/velocidad"

# --- Configuración Motores ---
MOTORES = {
    "A": {"in1": 14, "in2": 27, "pwm": 12},
    "B": {"in1": 26, "in2": 25, "pwm": 33},
    "C": {"in1": 32, "in2": 21, "pwm": 22},
    "D": {"in1": 19, "in2": 18, "pwm": 23},
}

# Velocidad inicial (0 - 1023)
VELOCIDAD_INICIAL = 512

# --- Debug ---
DEBUG = True   # Cambia a False para desactivar logs

# Otros actuadores
LED_PIN = 2
SERVO_PIN = 4

import network, time
from machine import Pin, PWM
from umqtt.simple import MQTTClient
import __config as config

# --- Función de log ---
def log(msg):
    if config.DEBUG:
        print(msg)

# --- Inicializar motores ---
motores = {
    nombre: {
        "in1": Pin(pines["in1"], Pin.OUT),
        "in2": Pin(pines["in2"], Pin.OUT),
        "pwm": PWM(Pin(pines["pwm"]), freq=1000)
    }
    for nombre, pines in config.MOTORES.items()
}

velocidad = config.VELOCIDAD_INICIAL

# --- WiFi con IP fija ---
def conectar_wifi_fija():
    sta = network.WLAN(network.STA_IF)
    sta.active(True)
    sta.ifconfig((config.IP_FIJA, config.MASK, config.GATEWAY, config.DNS))
    sta.connect(config.WIFI_SSID, config.WIFI_PASS)

    while not sta.isconnected():
        log("Conectando a WiFi...")
        time.sleep(1)

    log("✅ Conectado a WiFi con IP fija: " + sta.ifconfig()[0])
    return sta.ifconfig()[0]

# --- Motores ---
def configurar_motores(vel):
    for m in motores.values():
        m["pwm"].duty(vel)
    log(f"⚙️ PWM configurado en {vel}")

def detener_motores():
    for m in motores.values():
        m["in1"].value(0)
        m["in2"].value(0)
    log("🛑 Todos los motores detenidos")

def mover_motores(comando):
    log(f"➡️ Ejecutando comando: {comando}")

    if comando == "adelante":
        for m in motores.values():
            m["in1"].value(1); m["in2"].value(0)
    elif comando == "atras":
        for m in motores.values():
            m["in1"].value(0); m["in2"].value(1)
    elif comando == "izquierda":
        motores["A"]["in1"].value(0); motores["A"]["in2"].value(1)
        motores["B"]["in1"].value(0); motores["B"]["in2"].value(1)
        motores["C"]["in1"].value(1); motores["C"]["in2"].value(0)
        motores["D"]["in1"].value(1); motores["D"]["in2"].value(0)
    elif comando == "derecha":
        motores["A"]["in1"].value(1); motores["A"]["in2"].value(0)
        motores["B"]["in1"].value(1); motores["B"]["in2"].value(0)
        motores["C"]["in1"].value(0); motores["C"]["in2"].value(1)
        motores["D"]["in1"].value(0); motores["D"]["in2"].value(1)
    elif comando == "detener":
        detener_motores()

def ajustar_velocidad(valor):
    global velocidad
    try:
        velocidad = int(valor)
        velocidad = max(0, min(1023, velocidad))
        configurar_motores(velocidad)
        log(f"🚗 Velocidad ajustada a {velocidad}")
    except:
        log("⚠️ Error al ajustar velocidad")

# --- MQTT ---
def callback(topic, msg):
    log(f"📩 Mensaje recibido: {topic} -> {msg}")
    if topic == config.MQTT_TOPIC_DIR:
        mover_motores(msg.decode("utf-8"))
    elif topic == config.MQTT_TOPIC_VEL:
        ajustar_velocidad(msg)

def conectar_mqtt():
    cliente = MQTTClient(config.MQTT_CLIENT_ID, config.MQTT_BROKER)
    cliente.set_callback(callback)
    cliente.connect()
    cliente.subscribe(config.MQTT_TOPIC_DIR)
    cliente.subscribe(config.MQTT_TOPIC_VEL)
    log("✅ Conectado a broker MQTT y suscrito a topics")
    return cliente

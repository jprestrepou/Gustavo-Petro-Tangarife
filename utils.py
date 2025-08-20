def ejecutar_comando(comando, actuadores):
    if comando == "avanzar":
        for m in ["motor1", "motor2", "motor3", "motor4"]:
            actuadores[m].forward(512)
    elif comando == "retroceder":
        for m in ["motor1", "motor2", "motor3", "motor4"]:
            actuadores[m].backward(512)
    elif comando == "parar":
        for m in ["motor1", "motor2", "motor3", "motor4"]:
            actuadores[m].stop()
    elif comando == "led_on":
        actuadores["led"].on()
    elif comando == "led_off":
        actuadores["led"].off()
    elif comando.startswith("servo_"):
        angulo = int(comando.split("_")[1])
        actuadores["servo"].set_angle(angulo)
    else:
        print("Comando no reconocido.")

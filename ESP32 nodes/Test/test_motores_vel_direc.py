import time
import __functions as functions

def main():
    functions.conectar_wifi_fija()
    functions.configurar_motores(functions.velocidad)
    cliente = functions.conectar_mqtt()

    try:
        while True:
            cliente.check_msg()
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("🛑 Finalizando programa...")
        functions.detener_motores()
        cliente.disconnect()

if __name__ == "__main__":
    main()

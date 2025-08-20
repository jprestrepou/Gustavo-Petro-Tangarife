import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import paho.mqtt.client as mqtt

class NodoMotor(Node):
    def __init__(self):
        super().__init__('nodo_motor')

        # Suscripción al tópico ROS2
        self.subscription = self.create_subscription(
            String,
            '/motor/control',
            self.callback_motor,
            10
        )

        # Cliente MQTT
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.connect('localhost', 1883)  # o IP de tu broker
        self.get_logger().info('Nodo motor listo y conectado al broker MQTT.')

    def callback_motor(self, msg):
        comando = msg.data
        self.get_logger().info(f'Recibido comando motor: {comando}')

        # Enviar por MQTT
        self.mqtt_client.publish('robot/motor', comando)
        self.get_logger().info(f'Enviado por MQTT a robot/motor: {comando}')

def main(args=None):
    rclpy.init(args=args)
    nodo = NodoMotor()
    rclpy.spin(nodo)
    nodo.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

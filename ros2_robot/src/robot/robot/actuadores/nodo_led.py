import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import paho.mqtt.client as mqtt

class NodoLED(Node):
    def __init__(self):
        super().__init__('nodo_led')
        self.subscription = self.create_subscription(String, '/led/color', self.callback_led, 10)
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.connect('localhost', 1883)
        self.get_logger().info('NodoLED conectado a MQTT.')

    def callback_led(self, msg):
        self.mqtt_client.publish('robot/led', msg.data)
        self.get_logger().info(f'LED → {msg.data}')

def main(args=None):
    rclpy.init(args=args)
    node = NodoLED()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

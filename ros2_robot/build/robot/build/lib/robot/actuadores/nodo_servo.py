import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import paho.mqtt.client as mqtt

class NodoServo(Node):
    def __init__(self):
        super().__init__('nodo_servo')
        self.subscription = self.create_subscription(String, '/servo/angulo', self.callback_servo, 10)
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.connect('localhost', 1883)
        self.get_logger().info('NodoServo conectado a MQTT.')

    def callback_servo(self, msg):
        self.mqtt_client.publish('robot/servo', msg.data)
        self.get_logger().info(f'Servo → {msg.data}')

def main(args=None):
    rclpy.init(args=args)
    node = NodoServo()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

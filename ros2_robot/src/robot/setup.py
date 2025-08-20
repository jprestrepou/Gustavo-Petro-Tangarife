from setuptools import find_packages, setup
from glob import glob

package_name = 'robot'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', glob('launch/*.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='jpru',
    maintainer_email='jpru@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'nodo_ultrasonico = robot.sensores.nodo_ultrasonico:main',
            'nodo_lidar = robot.sensores.nodo_lidar:main',
            'nodo_imu = robot.sensores.nodo_imu:main',
            'nodo_motor = robot.actuadores.nodo_motor:main',
            'nodo_led = robot.actuadores.nodo_led:main',
            'nodo_servo = robot.actuadores.nodo_servo:main',
            'nodo_mqtt_rx = robot.comunicacion.nodo_mqtt_rx:main',
            'nodo_mqtt_tx = robot.comunicacion.nodo_mqtt_tx:main',
            'nodo_teleop_teclado = robot.interfaz.nodo_teleop_teclado:main',
            'nodo_monitor = robot.diagnostico.nodo_monitor:main',
            'nodo_navegacion = robot.planificacion.nodo_navegacion:main',
        ],
    },
)

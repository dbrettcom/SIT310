import socket
import threading
import time

import rclpy
from rclpy.node import Node

from drone_interfaces.srv import Move
from std_srvs.srv import Empty

# Gobal Variables for scaling letter/number sizing (small/medium/large)
sml = float(1);
med = float(1.25); #25% larger
lrg = float(1.5); #50% larger

# Change the scale below to select small, medium or large letters and numbers
Scale = med;

class DroneServer(Node):
    drone_response = "no_response"
    
    def __init__(self):
        super().__init__('drone_server')

        self.local_ip = ''
        self.local_port = 8889
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # socket for sending cmd
        self.socket.bind((self.local_ip, self.local_port))

        # thread for receiving cmd ack
        self.receive_thread = threading.Thread(target=self._receive_thread)
        self.receive_thread.daemon = True
        self.receive_thread.start()

        self.tello_ip = '192.168.10.1'
        self.tello_port = 8889
        self.tello_address = (self.tello_ip, self.tello_port)
        self.MAX_TIME_OUT = 15.0

        self.srv = self.create_service(Empty, 'takeoff', self.takeoff_callback)      
        self.srv = self.create_service(Empty, 'a', self.a_callback)
        self.srv = self.create_service(Empty, 'b', self.b_callback)
        self.srv = self.create_service(Empty, 'one', self.one_callback)
        self.srv = self.create_service(Empty, 'two', self.two_callback)
        self.srv = self.create_service(Empty, 'aOne', self.aOne_callback)
        self.srv = self.create_service(Empty, 'land', self.land_callback)
        
    def send_command(self, msg):
        command = msg #the actual command string
        self.get_logger().info('I heard: "%s"' % msg)
        self.socket.sendto(command.encode('utf-8'), self.tello_address)
        print('sending command: %s to %s' % (command, self.tello_ip))
        start = time.time()
        now = time.time()
        diff = now - start
        if diff > self.MAX_TIME_OUT:
            print('Max timeout exceeded... command %s' % command)
            return
        print('Done!!! sent command: %s to %s' % (command, self.tello_ip))

    def takeoff_callback(self, request, response):
        self.get_logger().info('Incoming request: Takeoff')
        command = "takeoff"
        print(command)
        self.send_command("command")
        time.sleep(2)
        self.send_command(command)
        return response

    def a_callback(self, request, response):
        global drone_response
        global Scale
        self.get_logger().info('Incoming request: Drawing the letter A at {} x scale'.format(Scale))
        command = "go {} {} {} {}".format(40*Scale, 80*Scale, 0*Scale, 50)
        print(command)
        self.send_command(command)
        time.sleep(4)
        command = "go {} {} {} {}".format(40*Scale, -80*Scale, 0*Scale, 50)
        print(command)
        self.send_command(command)
        time.sleep(4)
        command = "go {} {} {} {}".format(-20*Scale, 40*Scale, 0*Scale, 50)
        print(command)
        self.send_command(command)
        time.sleep(4)
        command = "go {} {} {} {}".format(-40*Scale, 0*Scale, 0*Scale, 50)
        print(command)
        self.send_command(command)
        time.sleep(4)
        command = "go {} {} {} {}".format(-20*Scale, -40*Scale, 0*Scale, 50)
        print(command)
        self.send_command(command)
        time.sleep(4)
        return response

    def b_callback(self, request, response):
        global drone_response
        global Scale
        self.get_logger().info('Incoming request: Drawing the letter B at {} x scale'.format(Scale))
        command = "go {} {} {} {}".format(0*Scale, 80*Scale, 0*Scale, 50)
        print(command)
        self.send_command(command)
        time.sleep(3)
        command = "curve {} {} {} {} {} {} {}".format(60*Scale, -20*Scale, 0*Scale, 0*Scale, -40*Scale, 0*Scale, 50)
        print(command)
        self.send_command(command)
        time.sleep(3)
        command = "curve {} {} {} {} {} {} {}".format(60*Scale, -20*Scale, 0*Scale, 0*Scale, -40*Scale, 0*Scale, 50)
        print(command)
        self.send_command(command)
        time.sleep(3)
        return response

    def c_callback(self, request, response):
        global drone_response
        global Scale
        self.get_logger().info('Incoming request: Drawing the letter C at {} x scale'.format(Scale))
        command = "curve {} {} {} {} {} {} {}".format(-60*Scale, 40*Scale, 0*Scale, 0*Scale, 80*Scale, 0*Scale, 50)
        print(command)
        self.send_command(command)
        time.sleep(3)
        # Retrace the letter C in reverse to get back to the starting location
        command = "curve {} {} {} {} {} {} {}".format(-60*Scale, -40*Scale, 0*Scale, 0*Scale, -80*Scale, 0*Scale, 50)
        print(command)
        self.send_command(command)
        time.sleep(3)
        return response

    def one_callback(self, request, response):
        global drone_response
        global Scale
        self.get_logger().info('Incoming request: Drawing the number 1 at {} x scale'.format(Scale))
        command = "go {} {} {} {}".format(0*Scale, 80*Scale, 0*Scale, 50)
        print(command)
        self.send_command(command)
        time.sleep(5)
        command = "go {} {} {} {}".format(-20*Scale, -20*Scale, 0*Scale, 50)
        print(command)
        self.send_command(command)
        time.sleep(5)
        # Retrace the number 1 in reverse to get back to the starting location
        command = "go {} {} {} {}".format(20*Scale, 20*Scale, 0*Scale, 50)
        print(command)
        self.send_command(command)
        time.sleep(5)
        command = "go {} {} {} {}".format(0*Scale, -80*Scale, 0*Scale, 50)
        print(command)
        self.send_command(command)
        time.sleep(5)
        return response

    def two_callback(self, request, response):
        global drone_response
        global Scale
        self.get_logger().info('Incoming request: Drawing the number 2 at {} x scale'.format(Scale))
        command = "go {} {} {} {}".format(-60*Scale, 0*Scale, 0*Scale, 50)
        print(command)
        self.send_command(command)
        time.sleep(4)
        command = "curve {} {} {} {} {} {} {}".format(38*Scale, 30*Scale, 0*Scale, 60*Scale, 68*Scale, 0*Scale, 50)
        print(command)
        self.send_command(command)
        time.sleep(4)
        command = "curve {} {} {} {} {} {} {}".format(-23*Scale, 15*Scale, 0*Scale, -60*Scale, 23*Scale, 0*Scale, 50)
        print(command)
        self.send_command(command)
        time.sleep(4)
        return response

    def three_callback(self, request, response):
        global drone_response
        global Scale
        self.get_logger().info('Incoming request: Drawing the number 3 at {} x scale'.format(Scale))
        command = "curve {} {} {} {} {} {} {}".format(60*Scale, 30*Scale, 0*Scale, 0*Scale, 60*Scale, 0*Scale, 50)
        print(command)
        self.send_command(command)
        time.sleep(3)
        command = "curve {} {} {} {} {} {} {}".format(60*Scale, 30*Scale, 0*Scale, 0*Scale, 60*Scale, 0*Scale, 50)
        print(command)
        self.send_command(command)
        time.sleep(3)
        # Retrace the number 3 in reverse to get back to the starting location
        command = "curve {} {} {} {} {} {} {}".format(60*Scale, -30*Scale, 0*Scale, 0*Scale, -60*Scale, 0*Scale, 50)
        print(command)
        self.send_command(command)
        time.sleep(3)
        command = "curve {} {} {} {} {} {} {}".format(60*Scale, -30*Scale, 0*Scale, 0*Scale, -60*Scale, 0*Scale, 50)
        print(command)
        self.send_command(command)
        time.sleep(3)
        return response

    def aOne_callback(self, request, response):
        self.a_callback(None, None)
        time.sleep(3)
        self.one_callback(None, None)
        time.sleep(3)
        return response

    def land_callback(self, request, response):
        self.get_logger().info('Incoming request: Land')
        command = "land"
        print(command)
        self.send_command("command")
        time.sleep(2)
        self.send_command(command)
        return response
    
    def _receive_thread(self):
        global drone_response
        #Listen to responses from the Tello.
        while True:
            try:
                self.response, ip = self.socket.recvfrom(1024)
                print('from %s: %s' % (ip, self.response))
                drone_response = str(self.response) #convert from byte string to string
            except (socket.error, exc):
                print("Caught exception socket.error : %s" % exc)

                

def main(args=None):
    rclpy.init(args=args)

    node = DroneServer()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    # Destroy the node explicitly
    # (optional - Done automatically when node is garbage collected)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

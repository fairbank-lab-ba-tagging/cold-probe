import serial
from time import sleep


class Arduino(object):
    """
    Class to communicate with the arduino.
        Handles all of the commands and serial communication
    """

    def __init__(self, comport, baudrate):
        self.comport = comport
        self.baudrate = baudrate

        self.port = None
        self.board_connected = False

    def connect(self):
        if self.board_connected:
            return True

        self.port = serial.Serial(self.comport, self.baudrate, timeout=3)

        sleep(3)

        cmd = 'Connect#'
        res = self.send(cmd)

        if res == 'Connected':
            self.board_connected = True
            return True
        else:
            return False

    def disconnect(self):
        if not self.board_connected:
            return True

        cmd = 'Disconnect#'
        res = self.send(cmd)
        if res == 'Disconnected':
            self.port.close()
            self.board_connected = False
            return True
        else:
            return False

    def digital_read(self, pin):
        self.check_connected()

        cmd = 'DigitalRead#{}$'.format(pin)
        try:
            res = int(self.send(cmd))
            return res
        except Exception:
            raise Exception("DigitalRead Failed!")

    def analog_read(self, pin):
        self.check_connected()

        cmd = 'AnalogRead#{}$'.format(pin)
        try:
            res = float(self.send(cmd))
            # print('Sent: {} \tReceived: {}'.format(cmd, res), end='\r')
            return res
        except Exception:
            raise Exception("AnalogRead Failed!")

    def digital_write(self, pin, val=1):
        self.check_connected()

        cmd = 'DigitalWrite#{}:{}$'.format(pin, val)
        res = self.send(cmd)
        if res == 'DigitalWrite':
            # print('Sent: {} \tReceived: {}'.format(cmd, res), end='\r')
            return True
        else:
            raise Exception("DigitalWrite Failed!")

    def send(self, cmd):
        send_bytes = str.encode(cmd)

        self.port.write(send_bytes)
        read_bytes = self.port.read_until(b'#')
        response = read_bytes.decode()

        return response[:-1]  # Get rid of the # at the end

    def check_connected(self):
        if self.board_connected and self.port.is_open:
            pass
        else:
            raise Exception("Not Connected!")

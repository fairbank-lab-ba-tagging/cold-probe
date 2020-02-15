import serial

port = serial.Serial('COM9', 57600)
port.write(b'Connect#')
for i in range(100):
    print(port.read(), end='')
port.close()

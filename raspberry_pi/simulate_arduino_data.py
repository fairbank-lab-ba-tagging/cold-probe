import serial
import numpy as np
from time import sleep

port = serial.Serial('/dev/pts/3', baudrate=19200, timeout=3.0)



while True:
    pressure = int(150 + np.random.rand() * 15)
    power = int(10 + np.random.rand()*6)
    other = np.random.randint(0, 1023, 4)

    counts = np.append(np.append(other, pressure), power)

    data = bytes(counts)
    sent = port.write(data)
    print('Sent {} bytes: {}'.format(len(data), counts))
    sleep(1)

import serial
import numpy as np

def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

port = serial.Serial('/dev/pts/2', baudrate=19200, timeout=3.0)

while True:
    counts = port.read(48)
    for chunk in chunks(counts, 8):
        print(int.from_bytes(chunk, byteorder='little'), end=', ')
    print()

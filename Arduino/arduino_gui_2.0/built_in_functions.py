from pyfirmata import INPUT, OUTPUT
from time import sleep, time


def ttl(pin, duration=0.01):
    pin.mode = OUTPUT
    pin.write(1)
    sleep(duration)
    pin.write(0)


def trigger(trigger):
    trigger.mode = INPUT
    while not trigger.read():
        sleep(0.001)


def move(start_pin, direction_pin, up, stop_trigger):
    # Prepare pin
    direction_pin.mode = OUTPUT
    print('Moving...')
    if up:
        direction_pin.write(1)
    else:
        direction_pin.write(0)
    ttl(start_pin)
    print('Move complete!')


def trigger_laser(pin, pulses, frequency):
    print('Triggering Laser')
    period = 1 / frequency
    last_pulse = 0
    i = 0
    while i < pulses:
        now = time()
        if now - last_pulse > period:
            ttl(pin, duration=0.01)
            last_pulse = now
            i += 1


def trigger_camera(pin, exposures, delay):
    print('Exposing {}'.format(exposures))
    for i in range(exposures - 1):
        print('Exp {}'.format(i + 1))
        ttl(pin)
        sleep(delay)
    print('Exp {}'.format(exposures))
    ttl(pin)

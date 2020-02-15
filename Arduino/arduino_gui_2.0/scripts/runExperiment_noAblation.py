from pyfirmata import INPUT, OUTPUT
from time import sleep, time


def run(board):
    analog_pins = board.analog_pins  # Pins 0-5
    digital_pins = board.digital_pins  # Pins 2-13

    # Stepper pins
    in_1 = digital_pins[2]
    in_2 = digital_pins[3]
    stepper_out = digital_pins[4]

    in_1.mode = OUTPUT
    in_2.mode = OUTPUT
    stepper_out.mode = INPUT

    # Laser pin
    laser_trigger = digital_pins[5]
    laser_trigger.mode = OUTPUT

    # Camera pin
    camera_trigger = digital_pins[6]
    camera_trigger.mode = OUTPUT

    # Prepare pins
    in_1.write(0)
    in_2.write(0)
    laser_trigger.write(0)
    camera_trigger.write(0)

    print('Start')

    duh = input('Send Down? [Enter]')

    send_down(in_1, in_2, stepper_out)

    duh = input('Send Up? [Enter]')

    send_up(in_1, in_2, stepper_out)

    # duh = input('Trigger Camera? [Enter]')

    ttl(camera_trigger)
    print('Picture Taken!')


# Defining functions to be used!!!

def ttl(pin, duration=0.01):
    pin.write(1)
    sleep(duration)
    pin.write(0)


def fire_laser(pin, pulses, frequency):
    period = 1 / frequency
    last_pulse = 0
    i = 0
    while i < pulses:
        now = time()
        if now - last_pulse > period:
            ttl(pin, duration=0.01)
            last_pulse = now
            i += 1


def trigger(trigger):
    while not trigger.read():
        sleep(0.001)


def send_up(start_pin, direction_pin, stop_trigger):
    print('Moving up...')
    start_time = time()
    direction_pin.write(1)
    ttl(start_pin)
    trigger(stop_trigger)
    stop_time = time()
    print('Move up complete! {:.4}s'.format(stop_time - start_time))


def send_down(start_pin, direction_pin, stop_trigger):
    print('Moving down...')
    start_time = time()
    direction_pin.write(0)
    ttl(start_pin)
    trigger(stop_trigger)
    stop_time = time()
    print('Move down complete! {:.4}s'.format(stop_time - start_time))

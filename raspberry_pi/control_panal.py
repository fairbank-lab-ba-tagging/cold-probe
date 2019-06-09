import tkinter as tk
import numpy as np
from sympy import sympify, symbols
from collections import deque
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import serial
import sys


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

class SerialMonitor():
    def __init__(self, port_path, num_bytes=48, baudrate=9600, timeout=0):
        self.port_path = port_path
        self.num_bytes = num_bytes
        self.baudrate = baudrate
        self.timeout = timeout

        self.port = serial.Serial(port_path, baudrate=baudrate, timeout=timeout)

    def read_data(self):
        counts = []
        data = self.port.read(self.num_bytes)
        for chunk in chunks(data, 8):
            counts.append(int.from_bytes(chunk, byteorder='little'))
        return counts


class PinMonitor():
    def __init__(self, key, frame, parent_frame, analog_num, label):
        self.key = key
        self.frame = frame
        self.parent_frame = parent_frame
        self.analog_num = analog_num
        self.label = label
        self.calibration = tk.StringVar()
        self.calibration.set('x')
        self.update_calibration()
        self.count = tk.IntVar()
        self.value = tk.DoubleVar()
        self.data_history = deque(maxlen=50)

        self.build_monitor()

    def build_monitor(self):
        info_frame = tk.Frame(master=self.frame, width=150)
        plot_frame = tk.Frame(master=self.frame)

        info_frame.grid(column=0, row=0, sticky='nsw')
        plot_frame.grid(column=1, row=0, sticky='w')

        main_label = tk.Label(master=info_frame, text=self.label)
        pin_label = tk.Label(master=info_frame, text='Analog Pin: {}'.format(self.analog_num))
        cal_label = tk.Label(master=info_frame, text='Calibration: ')
        cal_entry = tk.Entry(master=info_frame, textvariable=self.calibration)
        cal_submit = tk.Button(master=info_frame, text='OK', command=self.update_calibration)
        value_label = tk.Label(master=info_frame, textvariable=self.value)
        remove_monitor = tk.Button(master=info_frame, text='Remove Monitor', command=self.destroy)

        main_label.grid(column=0, row=0, columnspan=3)
        pin_label.grid(column=0, row=1, columnspan=3, sticky='nsw')
        cal_label.grid(column=0, row=2, sticky='nesw')
        cal_entry.grid(column=1, row=2, sticky='nesw')
        cal_submit.grid(column=2, row=2, sticky='nesw')
        value_label.grid(column=0, row=3, columnspan=3, sticky='nsw')
        remove_monitor.grid(column=0, row=4, columnspan=3, sticky='ns')

        fig = plt.figure(figsize=(12,1))
        self.ax = fig.add_subplot(111)
        self.line, = self.ax.plot(self.data_history)
        self.canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        canvas_widg = self.canvas.get_tk_widget()

        canvas_widg.pack(fill='both')

        self.frame.columnconfigure(1, weight=1)

    def destroy(self):
        self.parent_frame.remove_monitor(self.key)
        self.frame.destroy()

    def update(self):
        new_value = self.calibration_func.evalf(subs={x:self.count.get()})
        self.value.set(new_value)
        self.data_history.append(self.value.get())
        self.line.set_data(np.arange(0, len(self.data_history), 1), self.data_history)
        self.ax.set_xlim(0, len(self.data_history))
        self.ax.set_ylim(min(self.data_history)-1, max(self.data_history)+1)
        self.canvas.draw()

    def update_calibration(self):
        self.calibration_func = sympify(self.calibration.get())


class Mainframe(tk.Frame):
    def __init__(self, master, port_path):
        tk.Frame.__init__(self, master)
        self.master = master
        self.update_delay = 100 # milliseconds
        self.serial_monitor = SerialMonitor(port_path, num_bytes=48, baudrate=9600, timeout=0)
        self.pin_monitors = {}

        tk.Button(master=self.master, text="Add Pin Monitor", command=self.add_pin_monitor).pack()

        self.query_serial_port()

    def query_serial_port(self):
        if len(self.pin_monitors) > 0:
            serial_data = self.serial_monitor.read_data()
            if len(serial_data) > 0:
                for key in self.pin_monitors:
                    monitor = self.pin_monitors[key]
                    monitor.count.set(serial_data[monitor.analog_num])
                    monitor.update()
                print('Received data!')
                # print('No data received...')

        self.after(self.update_delay, self.query_serial_port)


    def add_pin_monitor(self):
        'Pop-up window for adding pin monitors.'
        x_pos = self.master.winfo_x()
        y_pos = self.master.winfo_y()
        popup = tk.Toplevel()

        pin_num = tk.IntVar()
        label = tk.StringVar()
        calibration = tk.StringVar()
        calibration.set('x')

        tk.Label(master=popup, text='Pin number (0-5):').grid(column=0, row=0, sticky='e')
        tk.Entry(master=popup, textvariable=pin_num).grid(column=1, row=0)
        tk.Label(master=popup, text='Monitor Label:').grid(column=0, row=1, sticky='e')
        tk.Entry(master=popup, textvariable=label).grid(column=1, row=1)
        tk.Button(master=popup, text='Cancel', command=lambda: self.cancel_add(popup)).grid(column=0, row=2)
        tk.Button(master=popup, text='Add Monitor', command=lambda: self.add_monitor(popup, pin_num, label)).grid(column=1, row=2)

        popup.geometry('+{}+{}'.format(x_pos + 100, y_pos + 100))

    def cancel_add(self, popup):
        popup.destroy()

    def add_monitor(self, popup, pin_num, label):
        i = 0
        while i < 100:
            if i not in self.pin_monitors:
                key = i
                break
            i += 1
        new_frame = tk.Frame(master=self.master, height=100, borderwidth=1, relief='raised')
        new_frame.pack()
        new_monitor = PinMonitor(key, new_frame, self, pin_num.get(), label.get())
        self.pin_monitors[key] = new_monitor
        print("New Monitor '{}' Pin: {}".format(new_monitor.label, new_monitor.analog_num))
        popup.destroy()
        print(self.pin_monitors)

    def remove_monitor(self, key):
        del self.pin_monitors[key]
        print(self.pin_monitors)


class App(tk.Tk):
    def __init__(self, port):
        tk.Tk.__init__(self)

        self.title('Cold Probe Controller')
        self.geometry('1000x600')
        self.grid()

        Mainframe(self, port)

        self.mainloop()



port_path = sys.argv[1]
print('Monitoring on {}'.format(port_path))
x = symbols('x')
plt.style.use('ggplot')
App(port_path)

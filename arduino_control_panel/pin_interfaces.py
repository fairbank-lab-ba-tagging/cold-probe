from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from importlib import import_module, reload
from datetime import datetime, timedelta
# from pyfirmata import INPUT, OUTPUT
from sympy import sympify, symbols
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
from collections import deque
from time import sleep, time
import tkinter as tk
import numpy as np
import sys
import csv
import os


class Interface():
    'General interface class to be extended'

    def __init__(self, key, board, frame, main_frame, label):
        self.key = key
        self.board = board
        self.frame = frame
        self.main_frame = main_frame
        self.label = label

    def destroy(self):
        'Remove from interface list and destroy'
        self.main_frame.remove_interface(self.key)
        self.frame.destroy()

    def update(self):
        'Should be overwritten by subclass'
        pass

    def popup_constructor(self):
        'Should be overwritten by subclass'
        pass


class Monitor(Interface):
    'Monitor the status of a given analog pin'

    def __init__(self, key, board, frame, main_frame, label, analog_pin_num):
        Interface.__init__(self, key, board, frame, main_frame, label)
        self.x = symbols('x')

        self.pin_num = analog_pin_num

        # Get the pin reference from the main_frame
        # self.pin = self.main_frame.analog_pins[self.pin_num]

        # String variable for the calibration
        self.calibration = tk.StringVar()
        self.calibration.set('x')

        # Data variables
        self.value = 0.0                 # Actual Value
        self.plot_every_holder = 1       # Holds the plot every till update
        self.value_str = tk.StringVar()  # For displaying value
        self.avg = tk.StringVar()        # For displaying average
        self.std = tk.StringVar()        # For displaying standard deviation
        self.save_path = tk.StringVar()  # Path to save file

        # Variables for plotting
        self.data_history = deque(maxlen=10000)
        self.time_history = deque(maxlen=10000)
        self.ymax = tk.DoubleVar()
        self.ymin = tk.DoubleVar()
        self.num_x = tk.IntVar()
        self.num_x.set(1000)
        self.plot_every = tk.DoubleVar()
        self.plot_every.set(1)
        self.last_plot = time()

        # Update calibration data now
        self.update_calibration()

        # Build the interface
        self.build_monitor()

    def build_monitor(self):
        # Two frames for into and plot
        info_frame = tk.Frame(master=self.frame, width=150)
        plot_frame = tk.Frame(master=self.frame)

        # Place frames
        info_frame.grid(column=0, row=0, sticky='nsw')
        plot_frame.grid(column=1, row=0, sticky='we')

        # Stuff for info frame
        main_label = tk.Label(master=info_frame, text=self.label)
        pin_label = tk.Label(master=info_frame, text='Pin: {}'.format(self.pin_num))
        cal_label = tk.Label(master=info_frame, text='Calibration: ')
        cal_entry = tk.Entry(master=info_frame, textvariable=self.calibration)
        cal_submit = tk.Button(master=info_frame, text='OK', command=self.update_calibration)
        value_label = tk.Label(master=info_frame, textvariable=self.value_str)
        avg_label = tk.Label(master=info_frame, textvariable=self.avg)
        std_label = tk.Label(master=info_frame, textvariable=self.std)
        remove_monitor = tk.Button(master=info_frame, text='Remove Monitor', command=self.destroy)

        # Place information
        main_label.grid(column=0, row=0, columnspan=3)
        pin_label.grid(column=0, row=1, columnspan=3, sticky='nsw')
        cal_label.grid(column=0, row=2, sticky='nesw')
        cal_entry.grid(column=1, row=2, sticky='nesw')
        cal_submit.grid(column=2, row=2, sticky='nesw')
        value_label.grid(column=0, row=3, sticky='nsw')
        avg_label.grid(column=1, row=3, sticky='nsw')
        std_label.grid(column=2, row=3, sticky='nsw')
        remove_monitor.grid(column=0, row=4, columnspan=3, sticky='ns')

        # Create options for plot
        plot_config_frame = tk.Frame(master=plot_frame, width=150)
        plot_config_frame.pack(side=tk.LEFT)

        num_x_label = tk.Label(master=plot_config_frame, text='Number of points:')
        plot_every_label = tk.Label(master=plot_config_frame, text='Plot Every (s):')
        num_x_entry = tk.Entry(master=plot_config_frame, width=8, textvariable=self.num_x)
        plot_every_entry = tk.Entry(master=plot_config_frame, width=8, textvariable=self.plot_every)
        save_entry = tk.Entry(master=plot_config_frame, textvariable=self.save_path)
        submit_button = tk.Button(master=plot_config_frame, text='Submit', command=self.update_plot)
        save_plot = tk.Button(master=plot_config_frame, text='Save Plot', command=self.save_plot)

        num_x_label.grid(column=0, row=0, sticky='e')
        num_x_entry.grid(column=1, row=0)
        plot_every_label.grid(column=0, row=1, sticky='e')
        plot_every_entry.grid(column=1, row=1)
        save_entry.grid(column=0, row=2, columnspan=2)
        save_plot.grid(column=0, row=3)
        submit_button.grid(column=1, row=3)

        # Create canvas for plot
        fig = plt.figure(figsize=(20, 1.2))
        self.ax = fig.add_subplot(111)
        self.line, = self.ax.plot(self.time_history, self.data_history)
        fig.subplots_adjust(bottom=0.2)
        plt.grid(True)
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        self.canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        canvas_widg = self.canvas.get_tk_widget()

        # Place canvas
        canvas_widg.pack(fill='both')

        self.frame.columnconfigure(1, weight=1)

    def update_plot(self):
        # self.ax.set_ylim(self.ymin.get(), self.ymax.get())
        self.plot_every_holder = self.plot_every.get()
        new_data_deque = deque(maxlen=self.num_x.get())
        new_time_deque = deque(maxlen=self.num_x.get())
        new_data_deque.extend(self.data_history)
        new_time_deque.extend(self.time_history)
        self.data_history = new_data_deque
        self.time_history = new_time_deque

    def save_plot(self):
        'Save current plot data to file'
        path = 'output_files\\{}'.format(self.save_path.get())  # fix for windows
        with open(path, 'w') as file:
            writer = csv.writer(file)
            writer.writerow(['time', self.label])
            writer.writerows(zip(self.time_history, self.data_history))
        print('Plot saved as {}'.format(path))

    def update_calibration(self):
        'Update the calibration function'
        self.calibration_func = sympify(self.calibration.get())
        self.data_history = deque(maxlen=self.data_history.maxlen)
        self.time_history = deque(maxlen=self.time_history.maxlen)
        # self.pin.mode = INPUT
        new_count = self.board.analog_read(self.pin_num)
        new_value = float(self.calibration_func.evalf(subs={self.x: new_count}))
        self.time_history.append(datetime.now())
        self.data_history.append(new_value)

    def popup_constructor(parent_popup, key, board, frame, main_frame, label):
        'Create popup to get Monitor information'
        # Find a good spot
        x_pos = parent_popup.winfo_x()
        y_pos = parent_popup.winfo_y()
        popup = tk.Toplevel(master=parent_popup)
        popup.geometry('+{}+{}'.format(x_pos + 10, y_pos + 10))

        pin_num_var = tk.IntVar()
        tk.Label(master=popup, text='Arduino Pin:').grid(column=0, row=0)
        tk.Entry(master=popup, textvariable=pin_num_var).grid(column=1, row=0)
        button = tk.Button(master=popup, text='Add', command=lambda: Monitor.construct_monitor(parent_popup,
                                                                                               key,
                                                                                               board,
                                                                                               frame,
                                                                                               main_frame,
                                                                                               label,
                                                                                               pin_num_var.get(),
                                                                                               popup))

        button.grid(column=0, row=1, columnspan=2, sticky='nesw')

    def construct_monitor(parent_popup, key, board, frame, main_frame, label, pin_num, last_popup):
        'Take information from the popup and instantiate the Monitor'
        new_monitor = Monitor(key, board, frame, main_frame, label, pin_num)
        main_frame.pin_interfaces[key] = new_monitor
        last_popup.destroy()
        parent_popup.destroy()

    def update(self):
        'Read data from the pin and process'
        # self.pin.mode = INPUT
        new_count = self.board.analog_read(self.pin_num)
        new_value = float(self.calibration_func.evalf(subs={self.x: new_count}))
        self.value = new_value
        self.value_str.set(str(new_value)[:6])

        if time() - self.last_plot > self.plot_every_holder:
            self.last_plot = time()
            self.data_history.append(new_value)
            self.time_history.append(datetime.now())

        self.avg.set(str(np.average(np.array(self.data_history)[-20:]))[:6])
        self.std.set(str(np.std(np.array(self.data_history)[-20:]))[:6])

        self.line.set_data(self.time_history, self.data_history)
        self.ax.set_xlim(min(self.time_history), max(self.time_history) + timedelta(seconds=1))
        self.ax.set_ylim(min(self.data_history) - 1, max(self.data_history) + 1)
        self.canvas.draw()


class Controller(Interface):
    'Used to control a single pin manually'

    def __init__(self, key, board, frame, main_frame, label, pin_num):
        Interface.__init__(self, key, board, frame, main_frame, label)

        self.pin_num = pin_num
        # self.pin = self.main_frame.digital_pins[self.pin_num]
        # self.pin.mode = OUTPUT

        self.status = False

        self.build_controller()

    def build_controller(self):
        # Two frames for into and current status
        info_frame = tk.Frame(master=self.frame, width=250)
        status_frame = tk.Frame(master=self.frame)

        # Place frames
        info_frame.pack(side=tk.LEFT)
        status_frame.pack(side=tk.LEFT)

        # information for info frame
        main_label = tk.Label(master=info_frame, text=self.label)
        pin_label = tk.Label(master=info_frame, text='Pin: {}'.format(self.pin_num))
        set_low = tk.Button(master=info_frame, text='LOW', command=self.set_low)
        set_high = tk.Button(master=info_frame, text='HIGH', command=self.set_high)
        send_ttl = tk.Button(master=info_frame, text='TTL', command=self.send_ttl)
        remove_monitor = tk.Button(master=info_frame, text='Remove Controller', command=self.destroy)

        # Place information
        main_label.grid(column=0, row=0, columnspan=3, sticky='ew')
        pin_label.grid(column=0, row=1, columnspan=3, sticky='nesw')
        set_low.grid(column=0, row=2, sticky='nesw')
        set_high.grid(column=1, row=2, sticky='nesw')
        send_ttl.grid(column=2, row=2, sticky='nsew')
        remove_monitor.grid(column=0, row=3, columnspan=3, sticky='ns')

        # Create icon for status
        self.green_icon = ImageTk.PhotoImage(Image.open('images/green_icon.png').resize((25, 25)))
        self.red_icon = ImageTk.PhotoImage(Image.open('images/red_icon.png').resize((25, 25)))

        self.status_label = tk.Label(master=status_frame, image=self.red_icon)
        self.status_label.photo = self.red_icon
        self.status_label.grid(column=0, row=0, sticky='w')

        self.frame.columnconfigure(1, weight=1)

    def set_low(self):
        # self.pin.mode = OUTPUT
        self.board.digital_write(self.pin_num, 0)
        self.status_label.config(image=self.red_icon)
        self.status_label.image = self.green_icon
        self.status = False
        print('Setting {} LOW'.format(self.pin_num))

    def set_high(self):
        # self.pin.mode = OUTPUT
        self.board.digital_write(self.pin_num, 1)
        self.status_label.config(image=self.green_icon)
        self.status_label.image = self.green_icon
        self.status = True
        print('Setting {} HIGH'.format(self.pin_num))

    def send_ttl(self):
        self.sent_ttl = True
        # self.pin.mode = OUTPUT
        self.set_high()
        sleep(0.001)
        self.set_low()

    def popup_constructor(parent_popup, key, board, frame, main_frame, label):
        x_pos = parent_popup.winfo_x()
        y_pos = parent_popup.winfo_y()

        popup = tk.Toplevel(master=parent_popup)
        popup.geometry('+{}+{}'.format(x_pos + 10, y_pos + 10))

        pin_num_var = tk.IntVar()
        tk.Label(master=popup, text='Arduino Pin:').grid(column=0, row=0)
        tk.Entry(master=popup, textvariable=pin_num_var).grid(column=1, row=0)
        button = tk.Button(master=popup, text='Add', command=lambda: Controller.construct_controller(parent_popup,
                                                                                                     key,
                                                                                                     board,
                                                                                                     frame,
                                                                                                     main_frame,
                                                                                                     label,
                                                                                                     pin_num_var.get(),
                                                                                                     popup))

        button.grid(column=0, row=1, columnspan=2, sticky='nesw')

    def construct_controller(parent_popup, key, board, frame, main_frame, label, pin_num, last_popup):
        new_controller = Controller(key, board, frame, main_frame, label, pin_num)
        main_frame.pin_interfaces[key] = new_controller
        last_popup.destroy()
        parent_popup.destroy()


class Timer(Interface):
    'Control a pin with a timer'

    def __init__(self, key, board, frame, main_frame, label, pin_num, delay, duration):
        Interface.__init__(self, key, board, frame, main_frame, label)

        self.pin_num = pin_num
        # self.pin = self.main_frame.digital_pins[self.pin_num]
        self.delay = tk.DoubleVar()
        self.duration = tk.DoubleVar()
        self.last_switch = datetime.now()

        self.delay.set(delay)
        self.duration.set(duration)

        self.new_delay = tk.DoubleVar()
        self.new_duration = tk.DoubleVar()

        self.time_till_change = tk.StringVar()

        self.status = False

        self.build_timer()

    def build_timer(self):
        # Two frames for into and current status
        info_frame = tk.Frame(master=self.frame, width=250)
        status_frame = tk.Frame(master=self.frame)

        # Place frames
        info_frame.pack(side=tk.LEFT)
        status_frame.pack(side=tk.LEFT)

        # information for info frame
        main_label = tk.Label(master=info_frame, text=self.label)
        pin_label = tk.Label(master=info_frame, text='Pin: {}'.format(self.pin_num))
        remove_monitor = tk.Button(master=info_frame, text='Remove Controller', command=self.destroy)

        # Place information
        main_label.grid(column=0, row=0, columnspan=2, sticky='ew')
        pin_label.grid(column=0, row=1, columnspan=2, sticky='nesw')
        remove_monitor.grid(column=0, row=2, columnspan=2, sticky='ns')

        # Delay Duration and status information
        icon_frame = tk.Frame(master=status_frame)
        times_frame = tk.Frame(master=status_frame)

        icon_frame.pack(side=tk.LEFT, fill=tk.Y)
        times_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.green_icon = ImageTk.PhotoImage(Image.open('images/green_icon.png').resize((25, 25)))
        self.red_icon = ImageTk.PhotoImage(Image.open('images/red_icon.png').resize((25, 25)))

        self.status_label = tk.Label(master=icon_frame, image=self.red_icon)
        self.status_label.photo = self.red_icon
        self.status_label.pack(side=tk.LEFT, fill=tk.Y)

        # Time stuff
        delay = tk.Label(master=times_frame, text='Delay (min)')
        duration = tk.Label(master=times_frame, text='Duration (min)')
        current_delay_label = tk.Label(master=times_frame, textvariable=self.delay)
        current_duration_label = tk.Label(master=times_frame, textvariable=self.duration)
        change_delay_entry = tk.Entry(master=times_frame, textvariable=self.new_delay)
        change_duration_entry = tk.Entry(master=times_frame, textvariable=self.new_duration)
        update_times_button = tk.Button(master=times_frame, text='OK', command=self.update_times)
        time_till_change_label = tk.Label(master=times_frame, textvariable=self.time_till_change)

        # Place these things
        delay.grid(column=0, row=0)
        duration.grid(column=1, row=0)
        current_delay_label.grid(column=0, row=1)
        current_duration_label.grid(column=1, row=1)
        change_delay_entry.grid(column=0, row=2)
        change_duration_entry.grid(column=1, row=2)
        update_times_button.grid(column=2, row=2)
        time_till_change_label.grid(column=0, row=3, columnspan=2)

    def update_times(self):
        self.delay.set(self.new_delay.get())
        self.duration.set(self.new_duration.get())

    def update(self):
        current_time = datetime.now()
        time_elapsed = current_time - self.last_switch
        if self.status:
            if time_elapsed > timedelta(minutes=self.duration.get()):
                self.set_low()
                self.last_switch = current_time
        else:
            if time_elapsed > timedelta(minutes=self.delay.get()):
                self.set_high()
                self.last_switch = current_time
        self.time_till_change.set(str(time_elapsed))

    def set_low(self):
        self.board.digital_write(self.pin_num, 0)
        self.status_label.config(image=self.red_icon)
        self.status_label.image = self.red_icon
        self.status = False
        print('Setting {} LOW'.format(self.pin_num))

    def set_high(self):
        self.board.digital_write(self.pin_num, 1)
        self.status_label.config(image=self.green_icon)
        self.status_label.image = self.green_icon
        self.status = True
        print('Setting {} HIGH'.format(self.pin_num))

    def popup_constructor(parent_popup, key, board, frame, main_frame, label):
        x_pos = parent_popup.winfo_x()
        y_pos = parent_popup.winfo_y()

        popup = tk.Toplevel(master=parent_popup)
        popup.geometry('+{}+{}'.format(x_pos + 10, y_pos + 10))

        pin_num_var = tk.IntVar()
        tk.Label(master=popup, text='Arduino Pin:').grid(column=0, row=0)
        tk.Entry(master=popup, textvariable=pin_num_var).grid(column=1, row=0, sticky='e')

        delay_var = tk.DoubleVar()
        tk.Label(master=popup, text='Delay between switches (min):').grid(column=0, row=1)
        tk.Entry(master=popup, textvariable=delay_var).grid(column=1, row=1, sticky='e')

        duration_var = tk.DoubleVar()
        tk.Label(master=popup, text='Duration (min):').grid(column=0, row=2, sticky='e')
        tk.Entry(master=popup, textvariable=duration_var).grid(column=1, row=2)

        button = tk.Button(master=popup, text='Add', command=lambda: Timer.construct_timer(parent_popup,
                                                                                           key,
                                                                                           board,
                                                                                           frame,
                                                                                           main_frame,
                                                                                           label,
                                                                                           pin_num_var.get(),
                                                                                           delay_var.get(),
                                                                                           duration_var.get(),
                                                                                           popup))

        button.grid(column=0, row=3, columnspan=2, sticky='nesw')

    def construct_timer(parent_popup, key, board, frame, main_frame, label, pin_num, delay, duration, last_popup):
        new_timer = Timer(key, board, frame, main_frame, label, pin_num, delay, duration)
        main_frame.pin_interfaces[key] = new_timer
        last_popup.destroy()
        parent_popup.destroy()


class ScriptRunner(Interface):
    'Receives a script and runs it, blocking till complete'

    def __init__(self, key, board, frame, main_frame, label):
        Interface.__init__(self, key, board, frame, main_frame, label)

        self.filename = tk.StringVar()
        self.filename.set('demo')

        self.build_scriptrunner()

    def build_scriptrunner(self):
        frame = tk.Frame(master=self.frame)
        frame.pack(fill='both')

        caution = '''Enter filename of script to run without ".py", must
contain a "run" function that takes only main_frame
object. Must be located in the scripts subdirectory:'''

        label = tk.Label(master=frame, text=self.label)
        prompt = tk.Label(master=frame, text=caution)
        remove = tk.Button(master=frame, text='Remove Script', command=self.destroy)
        entry = tk.Entry(master=frame, width=12, textvariable=self.filename)
        execute = tk.Button(master=frame, text='Execute', command=self.execute_script)

        label.grid(column=1, row=0, sticky='news')
        prompt.grid(column=0, row=0, rowspan=2, sticky='w')
        remove.grid(column=0, row=2)
        entry.grid(column=1, row=1, sticky='news')
        execute.grid(column=1, row=2, sticky='news')

    def popup_constructor(parent_popup, key, board, frame, main_frame, label):
        new_runner = ScriptRunner(key, board, frame, main_frame, label)
        main_frame.pin_interfaces[key] = new_runner
        parent_popup.destroy()

    def execute_script(self):
        filename = self.filename.get()
        exists = os.path.isfile('scripts\\' + filename + '.py')  # Fix for windows version!!!
        if exists:
            try:
                mod_path = 'scripts.{}'.format(filename)
                module = import_module(mod_path)
                reload(module)
                module.run(self.main_frame)
                # del sys.modules[mod_path]
                print('Script complete!')
            except:
                print('Error in running Script')
        else:
            print('File could not be found')


interface_types = {
    'Monitor': Monitor,
    'Controller': Controller,
    'Timer': Timer,
    'Script': ScriptRunner
}

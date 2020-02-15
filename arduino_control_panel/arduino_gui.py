from built_in_functions import move, trigger_laser, trigger_camera
from pin_interfaces import interface_types
from arduino_interface import Arduino
from PIL import Image, ImageTk
from datetime import datetime
import tkinter as tk
import json
import sys


class Mainframe(tk.Frame):
    'Class to hold the main window of the gui.'

    def __init__(self, root, board):
        tk.Frame.__init__(self, root)
        self.root = root

        # Prepare the board for use
        self.board = board
        self.board.connect()
        print("Board Connected: {}".format(self.board.board_connected))

        # Set main window features
        self.update_delay = 10  # milliseconds

        # Dictionary for holding and managing the active interfaces
        self.pin_interfaces = {}

        # Load data from config file
        # with open('config.json', 'r') as file:
        #     self.config = json.load(file)

        # store the active pins on the arduino
        # self.digital_pins = {}
        # self.analog_pins = {}
        #
        # for name in self.config['digital']:
        #     num = self.config['digital'][name]
        #     arduino_Pin = board.get_pin('d:{}:o'.format(num))
        #
        #     self.digital_pins[num] = MyPin(name, num, arduino_Pin)
        #
        # for name in self.config['analog']:
        #     num = self.config['analog'][name]
        #     arduino_Pin = board.get_pin('a:{}:i'.format(num))
        #
        #     self.analog_pins[num] = MyPin(name, num, arduino_Pin)
        #
        # # Set pins LOW as precaution
        # for pin_key in self.digital_pins:
        #     self.digital_pins[pin_key].write(0)
        # print('Digital pins set LOW.')

        # Icons for dashboard
        self.green_icon = ImageTk.PhotoImage(Image.open('images/green_icon.png').resize((25, 25)))
        self.red_icon = ImageTk.PhotoImage(Image.open('images/red_icon.png').resize((25, 25)))

        # Build the main window
        self.build_main_window()

    def build_main_window(self):
        # Create frame
        top_frame = tk.Frame(master=self.root)
        top_frame.pack(fill=tk.X)

        # Button for adding interfaces like monitors and controllers
        add_interface = tk.Button(master=top_frame, text="Add Pin Interface", command=self.add_interface_popup)
        add_interface.pack()

        # Build dash
        # dashboard = tk.Frame(master=top_frame, height=100, borderwidth=2, relief='raised')
        # dashboard.pack(fill=tk.X)
        #
        # digital_frame = tk.Frame(master=dashboard, height=50, borderwidth=1, relief='raised')
        # analog_frame = tk.Frame(master=dashboard, height=50, borderwidth=1, relief='raised')
        # function_frame = tk.Frame(master=dashboard, height=50, borderwidth=1, relief='raised')
        #
        # analog_frame.grid(column=0, row=0, stick='ew')
        # function_frame.grid(column=1, row=0, stick='ew')
        #
        # dashboard.columnconfigure([0, 1], weight=1)

        # Add analog pin stuff
        # for i, ana_key in enumerate(self.analog_pins):
        #     pin_frame = tk.Frame(master=analog_frame, width=50, borderwidth=1, relief='raised')
        #     pin_frame.grid(column=i, row=0, sticky='news')
        #
        #     value_str = tk.StringVar()
        #     value_str.set(self.analog_pins[ana_key].read())
        #     label_string = self.analog_pins[ana_key].label
        #     label = tk.Label(master=pin_frame, text=label_string)
        #     value = tk.Label(master=pin_frame, textvariable=value_str)
        #     self.analog_pins[ana_key].value_str = value_str
        #
        #     label.grid(column=0, row=0, sticky='news')
        #     value.grid(column=0, row=1, sticky='news')
        #
        #     pin_frame.columnconfigure(0, weight=1)
        #
        # analog_frame.columnconfigure([i for i in range(len(self.analog_pins))], weight=1)
        # analog_frame.rowconfigure(0, weight=1)
        #
        # # Add built in functions
        # frames = [tk.Frame(master=function_frame) for i in range(3)]
        #
        # # Move UP / Down
        # start_pin = self.digital_pins[self.config['digital']['Stepper in_1']]
        # direction_pin = self.digital_pins[self.config['digital']['Stepper in_2']]
        # stop_trigger = self.digital_pins[self.config['digital']['Stepper out_3']]
        #
        # def up_callback(): return move(start_pin, direction_pin, 1, stop_trigger)
        # up_button = tk.Button(master=frames[0], text='Move Up', command=up_callback)
        # up_button.pack()
        #
        # def down_callback(): return move(start_pin, direction_pin, 0, stop_trigger)
        # down_button = tk.Button(master=frames[0], text='Move Down', command=down_callback)
        # down_button.pack()
        #
        # # Trigger Laser
        # tk.Label(master=frames[1], text='Pulses').grid(column=0, row=1)
        # tk.Label(master=frames[1], text='Frequency').grid(column=1, row=1)
        #
        # pulses = tk.IntVar()
        # pulses.set(750)
        # frequency = tk.DoubleVar()
        # frequency.set(25)
        #
        # tk.Entry(master=frames[1], width=8, textvariable=pulses).grid(column=0, row=2)
        # tk.Entry(master=frames[1], width=8, textvariable=frequency).grid(column=1, row=2)
        #
        # laser_pin = self.digital_pins[self.config['digital']['Laser']]
        #
        # def laser_callback(): return trigger_laser(laser_pin, pulses.get(), frequency.get())
        # laser_button = tk.Button(master=frames[1], text='Trigger Laser', command=laser_callback)
        # laser_button.grid(column=0, row=0, columnspan=2)
        #
        # # Trigger Camera
        # tk.Label(master=frames[2], text='Exposures').grid(column=0, row=1)
        # tk.Label(master=frames[2], text='Delay').grid(column=1, row=1)
        #
        # exposures = tk.IntVar()
        # exposures.set(2)
        # delay = tk.DoubleVar()
        # delay.set(12)
        #
        # tk.Entry(master=frames[2], width=8, textvariable=exposures).grid(column=0, row=2)
        # tk.Entry(master=frames[2], width=8, textvariable=delay).grid(column=1, row=2)
        #
        # camera_pin = self.digital_pins[self.config['digital']['Camera']]
        #
        # def camera_callback(): return trigger_camera(camera_pin, exposures.get(), delay.get())
        # camera_button = tk.Button(master=frames[2], text='Trigger Camera', command=camera_callback)
        # camera_button.grid(column=0, row=0, columnspan=2)
        #
        # for i, frame in enumerate(frames):
        #     frame.grid(column=i, row=0, sticky='news')
        #
        # function_frame.columnconfigure([0, 1, 2], weight=1)

        # Enter the update loop (runs forever)
        self.update_interfaces()

    def update_interfaces(self):
        'Update the interfaces'
        # Loop through each interface and call its update function
        for key in self.pin_interfaces:
            self.pin_interfaces[key].update()

        # Update dashboard
        # self.update_dash()

        # After the set delay repeat the update
        self.after(self.update_delay, self.update_interfaces)

    def update_dash(self):
        for ana_key in self.analog_pins:
            my_pin = self.analog_pins[ana_key]
            value = my_pin.read()
            my_pin.value_str.set(value)

    def add_interface_popup(self):
        'Create a popup for selecting the type of interface to add'
        # Create popup in reasonable position
        x_pos = self.master.winfo_x()
        y_pos = self.master.winfo_y()
        popup = tk.Toplevel()
        popup.geometry('+{}+{}'.format(x_pos + 100, y_pos + 100))

        # Variables for new interface
        label = tk.StringVar()
        interface_type = tk.StringVar()
        interface_type.set('Monitor')

        # Construct the popup
        label_label = tk.Label(master=popup, text='Interface Label:')
        entry = tk.Entry(master=popup, textvariable=label)
        type_label = tk.Label(master=popup, text='Type:')
        options = tk.OptionMenu(popup, interface_type, 'Monitor', 'Controller', 'Timer', 'Script')
        cancel = tk.Button(master=popup, text='Cancel', command=lambda: self.cancel_add(popup))
        add = tk.Button(master=popup, text='Add Interface',
                        command=lambda: self.add_interface(popup, label, interface_type.get()))

        # Place widgets
        label_label.grid(column=0, row=0, sticky='e')
        entry.grid(column=1, row=0)
        type_label.grid(column=0, row=1, sticky='e')
        options.grid(column=1, row=1, sticky='ew')
        cancel.grid(column=0, row=2)
        add.grid(column=1, row=2)

    def cancel_add(self, popup):
        'Cancel the add interface'
        popup.destroy()

    def add_interface(self, popup, label, type):
        'Queue the popup for the requested interface'
        print('Creating {}'.format(type))

        # Find distinct key
        for i in range(100):
            if i not in self.pin_interfaces:  # if key not already in use
                key = i
                break

        # Create and place the new frame for the interface
        new_frame = tk.Frame(master=self.root, height=100, borderwidth=1, relief='raised')
        new_frame.pack(fill=tk.X)

        # Tell the new interface to build itself with this new frame and key
        interface = interface_types[type]
        interface.popup_constructor(popup, key, board, new_frame, self, label.get())

    def remove_interface(self, key):
        'Function to remove interfaces from the dictionary'
        del self.pin_interfaces[key]
        print(self.pin_interfaces)


class App(tk.Tk):
    'Application class'

    def __init__(self, board):
        tk.Tk.__init__(self)

        # Prepare the window
        self.title('Cold Probe Controller')
        self.geometry('1000x600')
        self.grid()
        self.board = board

        # Let the Mainframe do its thang
        Mainframe(self, board)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.mainloop()

    def on_closing(self):
        self.board.disconnect()
        self.destroy()


if __name__ == '__main__':
    board_path = sys.argv[1]
    print('Connecting to board at {}'.format(board_path))
    board = Arduino(board_path, 115200)
    print('Creating App')
    App(board)

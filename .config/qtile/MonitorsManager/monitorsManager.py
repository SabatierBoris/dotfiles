from os.path import expanduser
import pyudev
from modes import *

class Singleton(type):
    """
    Singleton pattern metaclass
    """
    def __init__(cls, name, bases, dict):
        super(Singleton, cls).__init__(name, bases, dict)
        cls.instance = None

    def __call__(cls, *args, **kw):
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__call__(*args, **kw)
        return cls.instance

class MonitorsManager(object):
    """
    Manage the monitors
    """
    __metaclass__ = Singleton

    def __init__(self,master="LVDS1",save_file="~/.monitorsManager"):
        self.screen = xrandr.get_current_screen()
        self.master = master
        self.save_file = save_file
        self.connected_monitors = None
        self.modes = None
        self.current_mode = None
        self.load_connected_monitor()
        self.master_output = None
        for output in self.connected_monitors:
            if output.name == self.master:
                self.master_output = output
                break
        if self.master_output == None:
            self.master_output = self.connected_monitor[0]
        self.check_current_mode()

    
        #Seting the udev drm event to check when a monitor is pluged/unpluged
        context = pyudev.Context()
        monitor = pyudev.Monitor.from_netlink(context)
        monitor.filter_by('drm')
        monitor.enable_receiving()

        #Observe if any monitors change
        observer = pyudev.MonitorObserver(monitor, self.check_current_mode)
        observer.start()

    def read_save_file(self):
        mode_name = None
        with open(expanduser(self.save_file),"r") as f:
            mode_name = f.readline()
        if mode_name:
            for mode in self.modes:
                if mode.name == mode_name:
                    self.current_mode = mode

    def write_save_file(self):
        with open(expanduser(self.save_file),"w") as f:
            f.write(self.current_mode.name)

    def load_connected_monitor(self):
        outputs = self.screen.get_outputs()
        self.connected_monitors = []
        for output in outputs:
            if output.is_connected():
                self.connected_monitors.append(output)
        
    def update_available_modes(self):
        self.modes = []
        if self.connected_monitors:
            nb_monitors = len(self.connected_monitors)

            # Only
            for output in self.connected_monitors:
                self.modes.append(SimpleMode(self.screen,
                                             "Only %s" % output.name,
                                             output,
                                             [i for i in self.connected_monitors if i != output]
                                    ))
                if nb_monitors >= 2:
                    if output != self.master_output:
                        # Clone
#                        self.modes.append(CloneMode(self.screen,
#                                                    "%s clone with %s" % (self.master,output.name),
#                                                    (self.master_output,output),
#                                                    [i for i in self.connected_monitors if i != output and i != self.master_output]
#                                         ))
                        # Extend
                        self.modes.append(ExtendMode(self.screen,
                                                     "%s extend to %s" % (self.master,output.name),
                                                     self.master_output,
                                                     output,
                                                     [i for i in self.connected_monitors if i != output and i != self.master_output]
                                         ))

    def get_next_mode(self,mode):
        next_mode = None
        if mode == None:
            next_mode = self.modes[0]
        else:
            prev = None
            for i in self.modes:
                if prev == mode:
                    next_mode = i
                prev = i
            if next_mode == None:
                next_mode = self.modes[0]
        return next_mode

    def switch_to_next_mode(self):
        next_mode = None
        if self.current_mode == None:
            next_mode = self.modes[0]
        else:
            prev = None
            for i in self.modes:
                if prev == self.current_mode:
                    next_mode = i
                prev = i
            if next_mode == None:
                next_mode = self.modes[0]
        self.switch_to(next_mode)

    def switch_to(self,mode):
        #print "Set : %s" % mode
        self.current_mode = mode
        self.write_save_file()
        mode.activate()

    def check_current_mode(self):
        self.load_connected_monitor()
        self.update_available_modes()
        self.read_save_file()
        if self.current_mode == None or self.current_mode not in self.modes:
            self.switch_to_next_mode()
        else:
            self.switch_to(self.current_mode)

from xrandr import xrandr

class Mode(object):
    """
    This is the base for the monitor management modes.
    It provide some common feature used by modes.
    """
    def __init__(self,screen,name):
        """
        @param screen instance of the xrandr screen
        @param name name of the mode
        """
        self.screen = screen
        self.name = name

    def turnOffOutput(self,output):
        """
        Shutdown one monitor
        """
        output.disable()

    def turnOff(self,outputs):
        """
        Shutdown a list of monitors
        """
        if outputs:
            for output in outputs:
                #print " -- turn off %s" % output.name
                self.turnOffOutput(output)

    def apply(self):
        """
        Validate the modification in the screen object
        """
        self.screen.apply_output_config()

    def activate(self):
        """
        This method should be overide by mode to implemente the monitor management
        """
        raise NotImplementedError("Abstract Method")

    def __str__(self):
        return "%s" % self.name

class SimpleMode(Mode):
    """
    This is a simple mode with only one monitor.
    All other monitor will be shutdown
    """
    def __init__(self,screen,name,master_output,others_outputs):
        """
        @param master_output This xrandr output object will be the active monitor
        @param others_outputs This list of output will be turn off
        """
        super(SimpleMode,self).__init__(screen,name)
        self.master_output = master_output
        self.others_outputs = others_outputs

    def activate(self):
        self.master_output.set_to_mode(0)
        self.apply()
        self.turnOff(self.others_outputs)
        self.apply()
        self.master_output.set_to_mode(0)
        self.apply()

class CloneMode(Mode):
    """
    This is a clone mode between two monitor
    """
    def __init__(self,screen,name,used_outputs,others_outputs):
        """
        @param used_outputs two monitors used
        @param others_outputs This list of output will be turn off
        """
        super(CloneMode,self).__init__(screen,name)
        self.used_outputs = used_outputs
        self.others_outputs = others_outputs

    def activate(self):
        #TODO This doesn't work for the moment
        #Detect the smaller monitor and apply this resolution to both with a scale ???
        self.used_outputs[0].set_to_mode(0)
        self.used_outputs[1].set_relation(self.used_outputs[0].name,
                                          xrandr.RELATION_SAME_AS)
        self.apply()
        self.turnOff(self.others_outputs)
        self.apply()



class ExtendMode(Mode):
    """
    This is a extend mode between a primary monitor and one other
    """
    def __init__(self,screen,name,primary_output,slave_output,others_outputs):
        """
        @param primary_output Main monitor
        @param slave_output Second monitor
        @param others_outputs This list of output will be turn off
        """
        super(ExtendMode,self).__init__(screen,name)
        self.primary_output = primary_output
        self.slave_output = slave_output
        self.others_outputs = others_outputs

    def activate(self):
        self.primary_output.set_to_mode(0)
        self.apply()
        self.slave_output.set_to_mode(0)
        self.slave_output.set_relation(self.primary_output.name,
                                       xrandr.RELATION_RIGHT_OF)
        self.apply()
        self.turnOff(self.others_outputs)
        self.apply()

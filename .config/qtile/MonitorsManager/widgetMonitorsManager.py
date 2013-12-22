from libqtile import bar
from libqtile.widget import base
import gobject
from monitorsManager import MonitorsManager

class WidgetMonitorsManager(base._TextBox):
    """
    Qtile widget for use the MonitorManager
    """
    def __init__(self,width=bar.CALCULATED, **config):
        self.manager = MonitorsManager()
        self.index = self.manager.current_mode
        self.idTimeout = None
        super(WidgetMonitorsManager,self).__init__("", width, **config)

    def apply(self,qtile=None):
        self.manager.switch_to(self.index)
        self.text = ""
        self.bar.draw() #Refresh the widget

    def next_mode(self,qtile=None):
        if self.idTimeout:
            gobject.source_remove(self.idTimeout)
        self.index = self.manager.get_next_mode(self.index)
        self.text = "%s" % (self.index)
        self.bar.draw() #Refresh the widget
        self.idTimeout = self.timeout_add(3,self.apply)

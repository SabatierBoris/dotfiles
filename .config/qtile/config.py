from libqtile.log_utils import init_log
from libqtile.config import Key, Screen, Group
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from MonitorsManager.widgetMonitorsManager import WidgetMonitorsManager

import subprocess, re


logger = init_log()

widMonitors = WidgetMonitorsManager()


#--------------HOOKS--------------
@hook.subscribe.screen_change
def restart_on_randr(qtile, ev):
    qtile.cmd_restart()

mod = "mod4"

keys = [
    # Backlight management
    Key(
        [], "XF86MonBrightnessUp",
        lazy.spawn("xbacklight -inc 10 -time 0; xbacklight > ~/.lastBackLight")
    ),
    Key(
        [], "XF86MonBrightnessDown",
        lazy.spawn("xbacklight -dec 10 -time 0; xbacklight > ~/.lastBackLight")
    ),
    # Switch between windows in current stack pane
    Key(
        [mod], "k",
        lazy.layout.down()
    ),
    Key(
        [mod], "j",
        lazy.layout.up()
    ),

    # Move windows up or down in current stack
    Key(
        [mod, "control"], "k",
        lazy.layout.shuffle_down()
    ),
    Key(
        [mod, "control"], "j",
        lazy.layout.shuffle_up()
    ),

    # Switch window focus to other pane(s) of stack
    Key(
        [mod], "space",
        lazy.layout.next()
    ),

    # Swap panes of split stack
    Key(
        [mod, "shift"], "space",
        lazy.layout.rotate()
    ),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"], "Return",
        lazy.layout.toggle_split()
    ),
    Key([mod], "Return", lazy.spawn("urxvt")),

    # Toggle between different layouts as defined below
    Key([mod], "Tab",    lazy.nextlayout()),
    Key([mod], "w",      lazy.window.kill()),

    Key([mod, "control"], "r", lazy.restart()),
    Key([mod], "r", lazy.spawncmd()),

    Key(
        [], "XF86Display",
        lazy.function(widMonitors.next_mode)
    ),
]

groups = [
    Group("a"),
    Group("s"),
    Group("d"),
    Group("f"),
    Group("u"),
    Group("i"),
    Group("o"),
    Group("p"),
]
for i in groups:
    # mod1 + letter of group = switch to group
    keys.append(
        Key([mod], i.name, lazy.group[i.name].toscreen())
    )

    # mod1 + shift + letter of group = switch to & move focused window to group
    keys.append(
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name))
    )

dgroups_key_binder = None
dgroups_app_rules = []

layouts = [
    layout.Max(),
    layout.Stack(stacks=2)
]

def get_screen_config(name):
    if name == "simple":
        ret = [
            Screen(
                top=bar.Bar(
                    [
                        widget.GroupBox(),
                        widget.Prompt(),
                        widget.WindowName(),
                        widget.TextBox("simple config", name="default"),
                        widMonitors,
                        widget.Systray(),
                        widget.Clock('%A %d/%m/%Y %H:%M'),
                    ],
                    24,
                )
            )
        ]
    elif name == "clone":
        ret = [
            Screen(
                top=bar.Bar(
                    [
                        widget.GroupBox(),
                        widget.Prompt(),
                        widget.WindowName(),
                        widget.TextBox("clone config", name="default"),
                        widget.Systray(),
                        widget.Clock('%A %d/%m/%Y %H:%M'),
                    ],
                    24,
                )
            )
        ]
    elif name == "extend":
        ret = [
            Screen(
                top=bar.Bar(
                    [
                        widget.GroupBox(),
                        widget.Prompt(),
                        widget.WindowName(),
                        widget.TextBox("extend config", name="default"),
                        widget.Systray(),
                        widget.Clock('%A %d/%m/%Y %H:%M'),
                    ],
                    24,
                )
            ),
            Screen(
                top=bar.Bar(
                    [
                        widget.GroupBox(),
                        widget.WindowName(),
                    ],
                    24,
                )
            )
        ]
    return ret


#s = lazy.screens()
#logger.error("%s" % s)
#c = s.check()
#logger.error("%s" % len(s))
#if s.length == 2:
screens = get_screen_config("simple")
#else:
#    screens = get_screen_config("simple")

follow_mouse_focus = True
cursor_warp = False
floating_layout = layout.Floating()
mouse = ()
auto_fullscreen = True
widget_defaults = dict(
        font = "MesloLGS",
        fontsize = 12,
        padding = 2,
)

def is_running(process):
    s = subprocess.Popen(["ps","axw"], stdout=subprocess.PIPE)
    for x in s.stdout:
        if re.search(process, x):
            return True
    return False

def execute_once(process):
    if not is_running(process):
        return subprocess.Popen(process.split())

@hook.subscribe.startup
def startup():
    logger.error("start")
    execute_once("touch /home/boris/toto")
    execute_once("xrdb ~/.Xresources")
    logger.error("end")


#def detect_screens(qtile):
#    """
#    Detect if a new screen is plugged and reconfigure/restart qtile
#    """
#    def setup_monitors(action=None, device=None):
#        """
#        Setup monitors
#        """
#        manager.check_current_mode()
#
#    setup_monitors()
#
#    import pyudev
#    
#    context = pyudev.Context()
#    monitor = pyudev.Monitor.from_netlink(context)
#    monitor.filter_by('drm')
#    monitor.enable_receiving()
#
#    #Observe if any monitors change
#    observer = pyudev.MonitorObserver(monitor, setup_monitors)
#    observer.start()
#
#def main(qtile):
#    startup(qtile)
#    detect_screens(qtile)

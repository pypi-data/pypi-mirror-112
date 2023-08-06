#!/usr/bin/env python3

"""
Iwdgui: A graphical frontend for iwd, Intel's iNet Wireless Daemon
(c) 2021 Johannes Willem Fernhout, BSD 3-Clause License applies
"""

BSD_LICENSE = """
Copyright 2021 Johannes Willem Fernhout <hfern@fernhout.info>.
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors
   may be used to endorse or promote products derived from this software
   without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE."""

import sys
import signal

try:
    from  netifaces import ifaddresses, AF_LINK, AF_INET, AF_INET6
except:
    sys.stderr.write("Please install netifaces")
    sys.exit(1)

try:
    import gi
    gi.require_version("Gtk", "3.0")
    from gi.repository import Gtk, GLib, Gio
except:
    sys.stderr.write("Please install gtk3 and python-gobject, or equivalent")
    sys.exit(1)

# own application packages
from . import pyiwd
from . import passwd_entry
from .comboboxtext import ComboBoxText

__VERSION__ = "0.1.0"
FRAME_LABEL_XALIGN = 0.025
VALUE_LEN = 36
PROMPT_LEN = 12
COMBOBOX_LEN = 64
PERIODIC_TICK = 10                     # call every so often in seconds
ICONNAME = "iwdgui"
BOTTOM = Gtk.PositionType.BOTTOM
RIGHT = Gtk.PositionType.RIGHT

def sigint_handler(sig, frame):      # frame is stack frame, and is ignored
    """ Signal handler for SIGINT, or Ctrl-C,
    to avoid standard Python stack dump """
    toplevels = Gtk.Window.list_toplevels()
    for toplevel in toplevels:
        toplevel.destroy()
    Gtk.main_quit()

def add_item2menu(mnu=None, label=None, action=None, data=None):
    """ adds a menuitem to a menu (mnu), optionally with an
    activate action and data to be passed to the action """
    if  mnu is None or label is None:
        print("add_item2menu: mnu nor label can be None", file=sys.stderr)
        raise AssertionError
    mni =  Gtk.MenuItem(label=label)
    if action:
        if data:
            mni.connect("activate", action, data)
        else:
            mni.connect("activate", action)
    mnu.append( mni )
    return mni

def addln2grid(grid, ln, label, widget):
    """ adds a line to a grid. ln is the last leftside widget to add
    below to label is the text of the prompt, widget is the value.
    Returns the labelwidget of the created prompt"""
    prompt = Gtk.Label(label=label.ljust(PROMPT_LEN),
                       xalign=0,
                       selectable=True,
                       width_chars=PROMPT_LEN,
                       max_width_chars=PROMPT_LEN)
    grid.attach_next_to(prompt, ln, BOTTOM, 1, 1)
    grid.attach_next_to(widget, prompt, RIGHT, 1, 1)
    return prompt

def get_netifaces_addr(iface, addr_type):

    try:
        #print("get_netifaces_addr, iface", iface, "addr_type", addr_type)
        addresses = ifaddresses(iface)[addr_type]
        return addresses
    except Exception as e:
        #print("Failed to get id address for", iface, " error:", e)
        return None

def icon_path(iconname, res):
    """ finds the path to an icon, based on std Gtk functions,
    so looking in standard locations like $HOME/.icons,
    $XDG_DATA_DIRS/icons, and /usr/share/pixmaps """
    icon_theme = Gtk.IconTheme.get_default()
    icon = icon_theme.lookup_icon(iconname, res, 0)
    if icon:
        path = icon.get_filename()
        return path
    return ""

def connection_str(b):
    "make a connection string from a bool"
    return "Connected" if b else "Not connected"

def start_scanning(dev_path):
    try:
        pyiwd.station_scan(dev_path)
    except Exception as e:
        #print("start_scanning exception:", e)
        pass


class GtkValueLabel(Gtk.Label):
    "Customized Gtk.Label class for width, alingment and selectable"
    def __init__(self):
        super().__init__()
        self.set_xalign(0)
        self.set_width_chars(VALUE_LEN)
        self.set_max_width_chars(VALUE_LEN)
        self.set_selectable(True)
        self.handle_nw_combobox_change = False


class IwdGuiWin(Gtk.Window):
    """ this is the main window if iwdgui """

    def __init__(self):
        Gtk.Window.__init__(self, title="Iwdgui", modal=True)
        self.set_default_size(150, 100)
        self.set_transient_for(None)
        self.set_keep_above(True)
        self.connect("destroy", Gtk.main_quit)
        self.box = None

        # define all class Gtk widgets here
        # Available networks frame

        # Device frame
        self.interface_combo = ComboBoxText()
        #self.scanning_checkbox = Gtk.CheckButton()
        self.ipv4_address = GtkValueLabel()
        self.ipv6_address = GtkValueLabel()

        # Connection status frame
        #self.network_combo = Gtk.ComboBoxText()
        self.network_combo = ComboBoxText()
        self.essid_label = GtkValueLabel()
        self.connection_state = GtkValueLabel()
        self.signal_strength_label = GtkValueLabel()
        self.sec_label = GtkValueLabel()

        # Known networks frame
        #self.known_network_combo = Gtk.ComboBoxText()
        self.known_network_combo = ComboBoxText()
        self.last_connected = GtkValueLabel()
        self.auto_connect = GtkValueLabel()
        self.known_nw_security = GtkValueLabel()
        self.hidden = GtkValueLabel()
        self.forget_network_button = Gtk.Button(label="Forget")
        self.forget_network_button.connect("clicked", self.forget_network)
        self.add_network_button = Gtk.Button(label=" Add ")
        self.add_network_button.connect("clicked", self.add_network)
        pyiwd.register_passwd_entry_callback(self.passwd_entry_callback)
        self.construct()
        pyiwd.register_props_changed_callback(
            self.handle_dbus_signal_properties_changed)
        #GLib.timeout_add(PERIODIC_TICK, self.periodic_props_update)
        GLib.timeout_add_seconds(PERIODIC_TICK, self.periodic_props_update)

    def dev_name(self):
        return self.interface_combo.get_active_text()

    def dev_path(self):
        return pyiwd.dev_path_by_name(self.dev_name())

    def nw_name(self):
        return self.network_combo.get_active_text()

    def nw_path(self):
        return pyiwd.nw_path_by_name(self.nw_name())

    def known_nw_name(self):
        return self.known_network_combo.get_active_text()

    def known_nw_path(self):
        return pyiwd.knonw_nw_path_by_name(self.known_nw_name())

    def construct(self):
        "Constructs the window contents"

        if self.box:
            self.box.destroy()
        self.box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)

        # build menu
        menubar = Gtk.MenuBar()
        applications_mni = add_item2menu(
            mnu=menubar, label="Application", action=None, data=None)
        # applications menu
        application_mnu = Gtk.Menu()
        about_mni = add_item2menu(
            mnu=application_mnu, label="About", action=self.about)
        quit_mnu = add_item2menu(
            mnu=application_mnu, label="Exit", action=self.app_exit)
        applications_mni.set_submenu(application_mnu)
        self.box.add(menubar)

        # interface frame
        device_frame = Gtk.Frame(label="Wireless interface",
                                 label_xalign=FRAME_LABEL_XALIGN)
        device_grid = Gtk.Grid(row_spacing=2, column_spacing=20)
        device_frame.add(device_grid)

        device_grid.attach_next_to(self.interface_combo, None,
                                   Gtk.PositionType.BOTTOM, 2, 1)
        self.populate_interface_combo_box()
        self.interface_combo.connect("changed", self.interface_combo_changed)
        ln = self.interface_combo
        ln = addln2grid(device_grid, ln, "IPv4 address", self.ipv4_address)
        ln = addln2grid(device_grid, ln, "IPv6 address", self.ipv6_address)

        # Active connection frame
        status_frame = Gtk.Frame(label="Active connection",
                                  label_xalign=FRAME_LABEL_XALIGN)
        status_grid = Gtk.Grid(row_spacing=2, column_spacing=20)
        status_frame.add(status_grid)
        status_grid.attach_next_to(self.network_combo, None,
                                   Gtk.PositionType.BOTTOM, 2, 1)
        self.install_network_combo_signal_handler()
        self.populate_network_combo_box()
        ln = self.network_combo
        ln = addln2grid(status_grid, ln, "Network name", self.essid_label)
        ln = addln2grid(status_grid, ln, "State", self.connection_state)
        ln = addln2grid(status_grid, ln,
                        "Signal strength", self.signal_strength_label)
        ln = addln2grid(status_grid, ln, "Security", self.sec_label)

        # known networks frame
        known_networks_frame = Gtk.Frame(label="Known networks",
                                         label_xalign=FRAME_LABEL_XALIGN)
        known_networks_grid = Gtk.Grid(row_spacing=2, column_spacing=20)
        known_networks_frame.add(known_networks_grid)
        known_networks_grid.attach_next_to(self.known_network_combo,
                                          None,
                                          Gtk.PositionType.BOTTOM, 2, 1)
        self.populate_known_network_combo_box()
        self.known_network_combo.connect("changed", 
                                          self.known_networks_combo_changed)
        ln = self.known_network_combo
        ln = addln2grid(known_networks_grid, ln,
                        "Last connected", self.last_connected)
        ln = addln2grid(known_networks_grid, ln,
                        "Auto connect", self.auto_connect)
        ln = addln2grid(known_networks_grid, ln,
                        "Security", self.known_nw_security)
        ln = addln2grid(known_networks_grid, ln, "Hidden", self.hidden)


        button_box = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
        button_box.pack_end(self.forget_network_button, False, True, 0)
        known_networks_grid.attach_next_to(button_box, self.hidden,
                                           Gtk.PositionType.BOTTOM, 1, 1)

        # build the window contents:
        self.box.add(Gtk.Label())
        self.box.add(device_frame)
        self.box.add(Gtk.Label())
        self.box.add(status_frame)
        self.box.add(Gtk.Label())
        self.box.add(known_networks_frame)
        self.box.add(Gtk.Label())

        self.unblock_network_combo_signal_handler()

        self.add(self.box)
        self.show_all()

    def manage_device_power(self):
        "Only can be powered on at the same time"
        device_list = pyiwd.dev_list()
        dev_name = self.dev_name()
        for device in device_list:
            device_path = pyiwd.dev_path_by_name(device["Name"])
            if device["Name"] == device["Name"]:
                start_scanning(device_path)
                self.connect_network()
            else:
                self.disconnect_network(device_path)

    def populate_interface_combo_box(self):
        "Populates the interface combo with connected devices"
        self.handle_nw_combobox_change = False
        device_list = pyiwd.dev_list()
        prev_dev_name = dev_name = self.dev_name()
        dev_path = None
        if dev_name:
            dev_path = self.dev_path()
        if not dev_path:
            if len(device_list) > 0:
                dev_name = device_list[0]["Name"]
                dev_path = pyiwd.dev_path_by_name(dev_name)
                #start_scanning(dev_path)
            else:
                print("Error: no iwd devices detected", file=sys.stderr)
                sys.exit(1)
        self.interface_combo.remove_all()
        active_assigned = False
        idx = 0 
        for device in device_list[::-1]:
            if device["Mode"] == 'station':
                self.interface_combo.append_text(device['Name'])
                if dev_name == device['Name']:
                    self.interface_combo.set_active(idx)
                    active_assigned = True
                idx += 1
        if self.dev_name() != prev_dev_name:
            self.populate_network_combo_box()
        if not active_assigned:
            self.interface_combo.set_active(0)
        self.manage_device_power()
        self.update_interface_status()
        self.handle_nw_combobox_change = True

    def interface_combo_changed(self, combobox):
        self.manage_device_power()
        self.update_interface_status()
        self.populate_network_combo_box()

    def update_interface_status(self):
        dev_name = self.dev_name()
        ipv4_addr = get_netifaces_addr(dev_name, AF_INET)
        if ipv4_addr:
            v4_addr = ipv4_addr[0]['addr']
        else:
            v4_addr = ""
        self.ipv4_address.set_text(v4_addr)
        ipv6_addr = get_netifaces_addr(dev_name,AF_INET6)
        if ipv6_addr:
            v6_addr = ipv6_addr[0]['addr']
        else:
            v6_addr = ""
        self.ipv6_address.set_text(v6_addr)

    def install_network_combo_signal_handler(self):
        self.network_combohandler = self.network_combo.connect(
            "changed", self.network_combo_change)

    def block_network_combo_signal_handler(self):

        """
        #self.network_combo.handler_disconnect(self.network_combohandler)
        self.network_combohandler.disconnect(self.network_combohandler)
        self.network_combohandler = None
        """

    def unblock_network_combo_signal_handler(self):
        """
        self.install_network_combo_signal_handler()
        """

    def populate_network_combo_box(self):
        if not self.dev_name():
            return
        self.handle_nw_combobox_change = False
        dev_name = self.dev_name()
        dev_path = self.dev_path()
        network_list = pyiwd.station_nws(dev_path)
        self.network_combo.remove_all()
        count = connected_network_idx = 0
        self.selected_network_key = None
        for network in network_list:
            network_dic = pyiwd.nw_dic_by_path(network[0])
            self.network_combo.append_text(network_dic["Name"])
            if network_dic["Connected"]:
                connected_network_idx = count
            count += 1
        self.unblock_network_combo_signal_handler()
        self.network_combo.set_active(connected_network_idx) 
        self.network_combo_exists = True
        self.update_network_props()
        self.handle_nw_combobox_change = True

    def network_combo_change(self, combobox):
        if not self.handle_nw_combobox_change:
            return
        self.connect_network()

    def update_network_props(self):
        #if not self.active_device or not self.active_network:
        #    return
        dev_path = self.dev_path()
        nw_name = self.nw_name()
        nw_path = self.nw_path()
        connected_nw_dic = pyiwd.nw_dic_by_path(nw_path)
        rssi = pyiwd.station_rrsi(dev_path, nw_path)
        self.essid_label.set_text(nw_name)
        self.connection_state.set_text(connection_str(
            connected_nw_dic["Connected"]))
        self.signal_strength_label.set_text(str(rssi) + " dBm")
        self.sec_label.set_text(connected_nw_dic["Type"])

    def handle_dbus_signal_properties_changed(self, interface,
                                             changed, invalidated, path):
        dev_path = self.dev_path()
        iface = interface[interface.rfind(".") + 1:]
        for name, value in changed.items():
            if name != "Scanning":
                print("{%s} [%s] %s = %s" % (iface, path, name, value))
            if iface == "Station":
                if path == dev_path:
                    if name == "State":
                        self.connection_state.set_text(value)
                    elif name == "Connected":
                        self.connection_state.set_text(connection_str(value))
                        #start_scanning(path)
                    elif name == "ConnectedNetwork":
                        network = pyiwd.nw_dic_by_path(value)
                        self.essid_label.set_text(network["Name"])
                        self.update_network_props()
                    elif name == "Scanning":
                        if not value:
                            nws_in_range = pyiwd.station_nws(dev_path)
                            entries = [pyiwd.nw_dic_by_path(nw[0])["Name"] \
                                for nw in nws_in_range]
                            self.network_combo.update_entries(entries)
                    else:
                        print("ERROR, station change not caught")
                else:
                    print("WANRING:, station change for non-acive device")
                    devdic = pyiwd.dev_dic_by_path(path)
                    devname = devdic["Name"]
                    if not devname in self.interface_combo.entries():
                        self.interface_combo.insert_text_sorted(devname)
                    if ((name == "Scanning" and value) or
                        (name == "State" and value == "connecting") or
                        (name == "ConnectedNetwork")):
                        self.disconnect_network(path)
            elif iface == "Network":
                if dev_path == pyiwd.nw_devpath_by_nwpath(path):
                    if name == "Connected":
                        self.connection_state.set_text(connection_str(value))
                    elif name == "KnownNetwork":
                        known_nw_list = pyiwd.known_nw_list()
                        entries = [nw["Name"] for nw in known_nw_list]
                        self.known_network_combo.update_entries(entries)
                    else:
                        print("network change not caught")
                else:
                    print("Network updatea for other dev ignored")
            elif iface == "KnownNetwork":
                print("known_network  update ignored")
            elif iface == "Device":
                if name == "Powered":
                    self.populate_interface_combo_box()
                print("Device change ignored")
            else:
                print("other update not caught")

    def passwd_entry_callback(self, path):
        nw_dic = pyiwd.nw_dic_by_path(path)
        return passwd_entry.show_password_entry_window(
            title=nw_dic["Name"])

    def connect_network(self):
        nw_path = self.nw_path()
        nw_name = self.nw_name()
        dev_path = self.dev_path()
        nw_dic = pyiwd.nw_dic_connected_to_dev(dev_path)
        if nw_path and nw_dic and nw_name != nw_dic["Name"]:
            pyiwd.nw_connect_async(nw_path,
                                   self.connect_reply_handler,
                                   self.connect_error_handler)

    def connect_reply_handler(self):
        "Called on connect success"
        print("connect_reply_handler")

    def connect_error_handler(self, error):
        "Called on connect failure"
        print("connect_error_handler", error)

    def disconnect_network(self, devpath):
        print("Disconnect network", devpath)
        pyiwd.station_disconnect_async(devpath,
                                       self.disconnect_network_success,
                                       self.disconnect_network_error)

    def disconnect_network_success(self):
        print("disconnect_network_success")

    def disconnect_network_error(self, error):
        print("disconnect_network_error:", error)

    def periodic_props_update(self):
        #print("*", end = '', sep = "", flush=True)
        dev_path = self.dev_path()
        start_scanning(dev_path)
        self.update_interface_status()
        return True

    def populate_known_network_combo_box(self):
        known_networks = pyiwd.known_nw_list()
        self.known_network_combo.remove_all()
        for known_network in known_networks:
            label = known_network["Name"]
            self.known_network_combo.append_text(known_network["Name"])
        self.known_network_combo.set_active(0)
        self.known_networks_combo_changed(self.known_network_combo)

    def known_networks_combo_changed(self, widget):
        known_network_name = widget.get_active_text()
        known_networks = pyiwd.known_nw_list()
        for known_network in known_networks:
            if known_network_name == known_network["Name"]:
                self.last_connected.set_text(known_network["LastConnectedTime"])
                self.auto_connect.set_text(
                    "yes" if known_network["AutoConnect"] else "no")
                self.known_nw_security.set_text(known_network["Type"])
                self.hidden.set_text(
                    "yes" if known_network["Hidden"] else "no")

    def forget_network(self, widget):
        known_network_name = self.known_network_combo.get_active_text()
        if known_network_name:
            known_network_path = pyiwd.known_nw_path_by_name(known_network_name)
            pyiwd.known_nw_forget(known_network_path)
            self.populate_known_network_combo_box()

    def add_network(self, widget):
        #print("add_network")
        pass

    def about(self, widget):
        """Shows the about dialog"""
        image = Gtk.Image()
        image.set_from_file(icon_path( ICONNAME, 96))
        icon_pixbuf = image.get_pixbuf()
        about_dialog = Gtk.AboutDialog()
        about_dialog.set_destroy_with_parent(True)
        about_dialog.set_logo(icon_pixbuf)
        about_dialog.set_program_name("Iwdgui")
        about_dialog.set_version("Version " + __VERSION__)
        about_dialog.set_comments("A graphical frontend for iwd, Intel's iNet Wireless Daemon")
        about_dialog.set_authors(["Johannes Willem Fernhout"])
        about_dialog.set_copyright( "(c) 2021 Johannes Willem Fernhout")
        about_dialog.set_license(BSD_LICENSE)
        about_dialog.set_website("https://gitlab.com/hfernh/iwdgui")
        about_dialog.set_website_label("iwdgui on GitLab")
        about_dialog.show_all()
        about_dialog.run()
        about_dialog.destroy()

    def app_exit(self, widget):
        Gtk.main_quit()


class IwdGuiApp(Gtk.Application):
    """" This is the main application class of iwdgui.
         It handles the standard signals for startup, activate
    """
    def __init__(self):
        Gtk.Application.__init__(self,
                                 application_id="org.gnome.example",
                                 flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.activated = False

    """ leave default handler in place for now
    def do_startup(self):
        print("do_startup") """

    def do_activate(self):
        if self.activated:                  # already running
            self.window.present()           # just set focus to our window
        else:
            self.window = IwdGuiWin()
            self.window.show()
            self.activated = True

def main():
    """ iwdgui main """
    # ignore GTK deprecation warnings gwhen not in development mode
    # for development mode, run program as python3 -X dev iwdgui
    if not sys.warnoptions:
        import warnings
        warnings.simplefilter("ignore")

    signal.signal(signal.SIGINT, sigint_handler)
    app = IwdGuiApp()
    app.run(sys.argv)
    Gtk.main()

if __name__ == "__main__":
    main()


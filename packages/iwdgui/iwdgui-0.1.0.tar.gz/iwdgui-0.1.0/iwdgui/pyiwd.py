#!/usr/bin/python3
"""
pyiwd: A graphical frontend for iwd, Intel's iNet Wireless Daemon.
(c) 2021 Johannes Willem Fernhout, BSD 3-Clause License applies.
"""

import os
import sys
import time
import json

try:
    import dbus
    import dbus.service
    from dbus.mainloop.glib import DBusGMainLoop
except:
    sys.stderr.write("Please install dbus-python")
    sys.exit(1)

IWD_PATH = "/net/connman/iwd"
IWD_SERVICE = "net.connman.iwd"
IWD_OBJECT_IF = "org.freedesktop.DBus.ObjectManager"
IWD_OBJECT_PATH = "/"
IWD_ADAPTER_IF = "net.connman.iwd.Adapter"
IWD_AGENT_IF = "net.connman.iwd.Agent"
IWD_AGENT_MGR_IF = "net.connman.iwd.AgentManager"
IWD_DEVICE_IF = "net.connman.iwd.Device"
IWD_KNOWN_NW_IF = "net.connman.iwd.KnownNetwork"
IWD_NW_IF = "net.connman.iwd.Network"
IWD_STATION_IF ="net.connman.iwd.Station"
DBUS_PROPERTIES = "org.freedesktop.DBus.Properties"
PYTHONDICS = 1

# Naming convention:
# - obj for object
# - dev for device
# - nw for network
# - adapter for adapter
# - station for station
# - known_nw for known_network
# - dic for dictionary
# - list for list
# - if for dbus interface

# init code and shorthands:
loop = DBusGMainLoop(set_as_default=True)

try:
    _bus = dbus.SystemBus()
except Exception as e:
    print("Cannot attach too dbus system bus:", e, file=sys.stderr)
    sys.exit(1)

#_dbus_if = lambda path, interface: dbus.Interface(
#    _bus.get_object(IWD_SERVICE, path), interface)
def _dbus_if(path, interface):
    try:
        return dbus.Interface(_bus.get_object(IWD_SERVICE, path), interface)
    except Exception as e:
        print("DBus interface error:", e, "(is iwd running?)", file=sys.stderr)
        sys.exit(1)

obj_if = _dbus_if(IWD_OBJECT_PATH, IWD_OBJECT_IF)
_obj_get = lambda: obj_if.GetManagedObjects()
_python_dics = lambda dics: json.loads(json.dumps(dics))
obj_get = lambda: _python_dics(_obj_get()) if PYTHONDICS else _obj_get()
_get_dic_by_path = lambda path, interface: obj_get()[path][interface]
props_if = lambda path: _dbus_if(path, DBUS_PROPERTIES)
register_props_changed_callback = lambda fn: _bus.add_signal_receiver(
    fn,
    bus_name=IWD_SERVICE,
    dbus_interface=DBUS_PROPERTIES, 
    signal_name="PropertiesChanged",
    path_keyword="path")


#network functions
nw_if = lambda path: _dbus_if(path, IWD_NW_IF)
nw_list = lambda: list(_objs_by_interface(IWD_NW_IF))
nw_dic_by_path = lambda path: _get_dic_by_path(path, IWD_NW_IF)
nw_path_by_name = lambda name: _get_path_by_name(name, IWD_NW_IF)
nw_devpath_by_nwpath = lambda path: os.path.dirname(path)
nw_list_connected = lambda: list(
    filter(lambda nw: nw['Connected'], nw_list()))

def nw_dic_connected_to_dev(path):
    for nw in nw_list_connected():
        if nw['Device'] == path:
            return nw
    return None

nw_connect_blocking = lambda path: nw_if(path).Connect()
nw_connect_async = lambda path, reply_handler, error_handler: \
    nw_if(path).Connect(reply_handler=reply_handler,
                             error_handler=error_handler)

#known network functions
known_nw_if = lambda path: _dbus_if(path, IWD_KNOWN_NW_IF)
known_nw_list = lambda: list(_objs_by_interface(IWD_KNOWN_NW_IF))
known_nw_path_by_name = lambda name: _get_path_by_name(
    name, IWD_KNOWN_NW_IF)
known_nw_dic_by_path = lambda path: _get_dic_by_path(path, IWD_KNOWN_NW_IF)
known_nw_forget = lambda path: known_nw_if(path).Forget()
known_nw_autoconnect = lambda path, value: props_if(path).Set(
    IWD_KNOWN_NW_IF, "AutoConnect", dbus.Boolean(value))
known_nw_autoconnect_on = lambda path: known_nw_autoconnect(
    path, True)
known_nw_autoconnect_off = lambda path: known_nw_autoconnect(
    path, False)

#station functions
station_if = lambda path: _dbus_if(path, IWD_STATION_IF)
station_list = lambda: list(_objs_by_interface(IWD_STATION_IF))
station_dic_by_path = lambda path: _get_dic_by_path(path, IWD_STATION_IF)
station_scan = lambda path: station_if(path).Scan()
_station_nws = lambda path: station_if(path).GetOrderedNetworks()
station_nws = lambda path: _python_dics(_station_nws(path)) \
    if PYTHONDICS else _station_nws(path)

def station_rrsi(dev_path, nw_path):
    #station_props = station_networks
    for path, rssi in station_nws(dev_path):
        if nw_path == path:
            return rssi

station_disconnect_blocking = lambda path: station_if(path).Disconnect()
station_disconnect_async = lambda path, reply_handler, error_handler: \
    station_if(path).Disconnect(reply_handler=reply_handler,
                                error_handler=error_handler)

#device functions
dev_if = lambda path: _dbus_if(path, IWD_DEVICE_IF)
dev_list = lambda: list(_objs_by_interface(IWD_DEVICE_IF))
dev_path_by_name = lambda name: _get_path_by_name( name, IWD_DEVICE_IF)
dev_dic_by_path = lambda path: _get_dic_by_path(path, IWD_DEVICE_IF)
dev_set_power = lambda path, value: props_if(path).Set(
    IWD_DEVICE_IF, "Powered", dbus.Boolean(value))
dev_set_power_on = lambda path: dev_set_power(path, True)
dev_set_power_off = lambda path: dev_set_power(path, False)
dev_set_mode = lambda path, mode: props_if(path).Set(
    IWD_DEVICE_IF, "Mode", mode)
dev_set_ap_mode = lambda path: dev_set_mode(path, 'ap')
dev_set_adhoc_mode = lambda path: dev_set_mode(path, 'ad-hoc')
dev_set_station_mode = lambda path: dev_set_mode(path, 'station')

#adapter functions
adapter_if = lambda path: _dbus_if(path, IWD_ADAPTER_IF)
adapter_list = lambda: list(_objs_by_interface(IWD_ADAPTER_IF))
adapter_path_by_name = lambda name: _get_path_by_name( name, IWD_ADAPTER_IF)
adapter_dic_by_path = lambda path: _get_dic_by_path(path, IWD_ADAPTER_IF)
adapter_set_power = lambda path, value: props_if(path).Set(
    IWD_ADAPTER_IF, "Powered", dbus.Boolean(value))
adapter_set_power_on = lambda path: adapter_set_power(path, True)
adapter_set_power_off = lambda path: adapter_set_power(path, False)

def _objs_by_interface(interface):
    "Yields the dictionary objects matching an interface spec "
    objects = obj_get()
    for elem in objects:
        for elem2 in objects[elem]:
            dic2 = objects[elem]
            if elem2 == interface:
                yield(dic2[elem2])

def _get_path_by_name(name, interface):
    #objects =list(_objs_by_interface(interface))
    objects = obj_get()
    """
    for obj in objects:
        if obj["Name"] == name:
            return obj
    """
    for elem in objects:
        dic2 = objects[elem]
        for elem2 in dic2:
            if (elem2 == interface and
                dic2[elem2]["Name"] == name):
                return elem
    return None

# agent and agent manager functions
agent_manager_if = _dbus_if(IWD_PATH, IWD_AGENT_MGR_IF)



class Agent(dbus.service.Object):
    "Agent class to handle callbacks in case iwd needs a user entry passwd"
    def __init__(self, passwd_entry_callback):
        global _bus
        self._path = '/test/agent/' + str(int(round(time.time() * 1000)))
        dbus.service.Object.__init__(self, _bus, self._path)
        self.passwd_entry_callback = passwd_entry_callback

    @property
    def path(self):
        return self._path

    @dbus.service.method(IWD_AGENT_IF, in_signature='', out_signature='')
    def Release(self):
        "So far I have not seen this being called"
        print("Agent released")

    @dbus.service.method(IWD_AGENT_IF, in_signature='o', out_signature='s')
    def RequestPassphrase(self, path):
        "This one gets called when trying to connect to a new network"
        #print("Agent: RequestPassphrase", path)
        return self.passwd_entry_callback(path)

    @dbus.service.method(IWD_AGENT_IF, in_signature='o', out_signature='s')
    def RequestPrivateKeyPassphrase(self, path):
        "So far I have not seen this being called"
        print("RequestPrivateKeyPassphrase", path)
        return self.passwd_entry_callback(path)

    @dbus.service.method(IWD_AGENT_IF, in_signature='o', out_signature='s,s')
    def RequestUserNameAndPassword(self, path, ):
        "So far I have not seen this being called"
        print("RequestUserNameAndPassword", path)
        return self.passwd_entry_callback(path)

    @dbus.service.method(IWD_AGENT_IF, in_signature='os', out_signature='s')
    def RequestUserPassword(self, path, username):
        "So far I have not seen this being called"
        print("RequestUserPassword", path, username)
        return self.passwd_entry_callback(path)

    @dbus.service.method(IWD_AGENT_IF, in_signature='s')
    def Cancel(self, reason ):
        "So far I have not seen this being called"
        print("Cancel", reason)
        return

def register_passwd_entry_callback(passwd_entry_callback):
    "registers a callback for whenever iwd needs passwd entry"
    global _bus, agent_manager_if
    agent = Agent(passwd_entry_callback)
    agent_manager_if.RegisterAgent(agent.path)


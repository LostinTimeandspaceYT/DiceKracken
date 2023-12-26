"""
Credit:
https://github.com/getis/micropython-web-control-panel/blob/main/WiFiConnection.py

"""
from micropython import const
from time import sleep_ms
import network
from web_api.network_credentials import NetworkCredentials


_STAT_WRONG_PASSWORD = const(-3) # failed due to incorrect password
_STAT_NO_AP_FOUND = const(-2)    # failed because no access point replied
_STAT_CONNECT_FAIL = const(-1)   # failed due to other problems
_STAT_IDLE = const(0)            # no connection and no activity
_STAT_CONNECTING = const(1)      # connecting in progress
_STAT_GOT_IP = const(3)          # connection successful


class WiFiConnection:
    status = network.STAT_IDLE
    ip = ""
    subnet_mask = ""
    gateway = ""
    dns_server = ""
    wlan = None

    def __init__(self) -> None:
        pass


    @classmethod
    def start_station_mode(cls, print_progress=False) -> bool:
        cls.wlan = network.WLAN(network.STA_IF)
        cls.wlan.active(True)
        cls.wlan.connect(NetworkCredentials.ssid, NetworkCredentials.password)
        cls.status = network.STAT_CONNECTING

        if print_progress:
            print("Attempting to connect, please wait")
        
        max_wait = 20

        while max_wait > 0:
           cls.status = cls.wlan.status()
           if _STAT_IDLE< cls.status >= _STAT_GOT_IP:
                break
           
           max_wait -= 1
           sleep_ms(500)
        
        cls.status = cls.wlan.status()
        
        if cls.status != _STAT_GOT_IP:
            if print_progress:
                print("Connection failed")
            return False
        
        else:
            config = cls.wlan.ifconfig()
            cls.ip = config[0]
            cls.subnet_mask = config[1]
            cls.gateway = config[2]
            cls.dns_server = config[3]
            if print_progress:
                print("IP: "+ str(cls.ip))
            return True


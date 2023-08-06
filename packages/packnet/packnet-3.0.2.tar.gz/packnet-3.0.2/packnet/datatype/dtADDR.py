"""

 PACKNET  -  c0mplh4cks

 DATATYPE
    ADDR



"""





# === Importing Dependencies === #
from struct import pack, unpack
from . import IP, MAC, INT







# === ADDR === #
class ADDR:
    def __init__(self, ip="255.255.255.255", port=0, mac="ff:ff:ff:ff:ff:ff", version=4, size=2):
        self.__ip = IP( ip, version=version )
        self.__port = INT( port, size=size )
        self.__mac = MAC( mac )


    def __str__(self):
        return f"['{self.ip}', {self.port}, '{self.mac}']"


    def __getitem__(self, key):
        if key == 0 or key == "ip":
            return self.ip
        elif key == 1 or key == "port":
            return self.port
        elif key == 2 or key == "mac":
            return self.mac
        else:
            raise IndexError


    def __setitem__(self, key, value):
        if key == 0 or key == "ip":
            self.ip = value
        elif key == 1 or key == "port":
            self.port = value
        elif key == 2 or key == "mac":
            self.mac = value
        else:
            raise IndexError



    @property
    def ip(self):
        return self.__ip


    @ip.setter
    def ip(self, value):
        if type(value) == str:
            self.__ip.ip = value
        elif type(value) == IP:
            self.__ip = value


    @property
    def port(self):
        return self.__port


    @port.setter
    def port(self, value):
        if type(value) == str:
            self.__port.integer = value
        elif type(value) == INT:
            self.__port = value


    @property
    def mac(self):
        return self.__mac


    @mac.setter
    def mac(self, value):
        if type(value) == str:
            self.__mac.mac = value
        elif type(value) == MAC:
            self.__mac = value


    @property
    def addr(self):
        return [ str(self.ip), int(self.port), str(self.mac) ]


    @addr.setter
    def addr(self, value):
        self.ip, self.port, self.mac = value

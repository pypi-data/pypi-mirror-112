"""

 PACKNET  -  c0mplh4cks

 DATATYPE
    MAC



"""





# === Importing Dependencies === #
from struct import pack, unpack







# === MAC === #
class MAC:
    def __init__(self, mac=""):
        self.mac = mac


    def __str__(self):
        return f"{self.mac}"


    def __len__(self):
        return 6



    @property
    def mac(self):
        return self.__mac


    @mac.setter
    def mac(self, value):
        self.__mac = value if type(value) != bytes else self.decode(value)[1]



    @staticmethod
    def decode(encoded):
        encoded = encoded[:6]
        mac = ":".join( ["{:02x}".format(n) for n in encoded] )
        return len(encoded), mac


    @staticmethod
    def encode(mac):
        encoded = b"".join( [pack(">B", int(n, 16)) for n in mac.split(":")] )
        return encoded


    def to_bytes(self, *args, **kwargs):
        return self.encode( self.mac )


    def from_bytes(self, encoded, *args, **kwargs):
        length, self.mac = self.decode(encoded)
        return length, self.mac

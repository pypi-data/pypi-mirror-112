"""

 PACKNET  -  c0mplh4cks

 DATATYPE
    IP



"""





# === Importing Dependencies === #
from struct import pack, unpack







# === IP === #
class IP:
    def __init__(self, ip="", version=4):
        self.ip = ip
        self.version = version


    def __str__(self):
        return f"{self.ip}"


    def __len__(self):
        return len( self.to_bytes() )



    @property
    def ip(self):
        return self.__ip


    @ip.setter
    def ip(self, value):
        if type(value) == str:
            self.__ip = value
            self.version = 4 if "." in value else 6

        elif type(value) == bytes:
            if self.version == 4:
                self.__ip = self.decodev4(value)[1]

            elif self.version == 16:
                self.__ip = self.decodev6(value)[1]



    @staticmethod
    def decodev4(encoded):
        encoded = encoded[:4]
        ip = ".".join( [str(n) for n in encoded] )
        return len(encoded), ip


    @staticmethod
    def encodev4(ip):
        encoded = b"".join( [pack(">B", int(n)) for n in ip.split(".")] )
        return encoded


    @staticmethod
    def encodev6(ip):
        ip = ip.split(":")

        if "" in ip:
            n = ip.index("")
            for i in range( 9-len(ip) ):
                ip.insert(n, "0")
            ip.remove("")

        return b"".join([ pack(">H", int(i, 16)) for i in ip ])


    @staticmethod
    def decodev6(encoded):
        ip = encoded[:16]
        parts = [ ip[i:i+2] for i in range(0, len(ip), 2) ]
        parts = [ hex(unpack(">H", p)[0])[2:] for p in parts ]
        ip = ":".join(parts)
        for i in range(6, 0, -1):
            z = ":0" * i
            if z in ip:
                ip = ip.replace(z, ":", 1)
        return len(encoded), ip



    def to_bytes(self, *args, **kwargs):
        if self.version == 4:
            return self.encodev4( self.ip )
        elif self.version == 6:
            return self.encodev6( self.ip )


    def from_bytes(self, encoded, *args, **kwargs):
        if self.version == 4:
            length, self.ip = self.decodev4(encoded)
        elif self.version == 6:
            length, self.ip = self.decodev6(encoded)
        return length, self.ip

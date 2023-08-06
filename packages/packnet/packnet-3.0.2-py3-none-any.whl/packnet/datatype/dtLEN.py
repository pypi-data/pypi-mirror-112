"""

 PACKNET  -  c0mplh4cks

 DATATYPE
    LEN



"""





# === Importing Dependencies === #
from struct import pack, unpack
from . import INT







# === LEN === #
class LEN:
    def __init__(self, header=0, payload=0, total=0, size=2):
        self.header = INT( 0 )
        self.payload = INT( 0 )
        self.__total = INT( 0 )
        self.size = size


    def __str__(self):
        return f"({self.header}, {self.payload}, {self.total})"


    def __getitem__(self, key):
        if key == 0 or key == "header":
            return self.header
        elif key == 1 or key == "payload":
            return self.payload
        elif key == 2 or key == "total":
            return self.total
        else:
            raise IndexError


    def __setitem__(self, key, value):
        if key == 0 or key == "header":
            self.header = value
        elif key == 1 or key == "payload":
            self.payload = value
        elif key == 2 or key == "total":
            self.total = value
        else:
            raise IndexError



    @property
    def size(self):
        return self.__size


    @size.setter
    def size(self, value):
        self.__size = value
        self.header.size = value
        self.payload.size = value
        self.total.size = value


    @property
    def total(self):
        self.__total.integer = (self.header.integer + self.payload.integer)
        return self.__total


    @total.setter
    def total(self, value):
        self.__total.integer = value.integer

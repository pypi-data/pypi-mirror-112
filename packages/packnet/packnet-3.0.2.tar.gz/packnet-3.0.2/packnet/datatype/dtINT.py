"""

 PACKNET  -  c0mplh4cks

 DATATYPE
    INT



"""







# === INT === #
class INT:
    def __init__(self, integer=0, size=2, format="big"):
        self.format = format
        self.size = size
        self.integer = integer


    def __str__(self):
        return f"{self.integer}"


    def __int__(self):
        return self.integer


    def __len__(self):
        return len( self.to_bytes() )



    @property
    def integer(self):
        return self.__integer


    @integer.setter
    def integer(self, value):
        self.__integer = value if type(value) != bytes else self.decode(value, self.size, self.format)[1]



    @staticmethod
    def encode(integer, size=2, format="big"):
        return integer.to_bytes( size, format )


    @staticmethod
    def decode(encoded, size=2, format="big"):
        encoded = encoded[:size]
        integer = int().from_bytes( encoded, format )
        return len(encoded), integer


    def to_bytes(self, *args, **kwargs):
        return self.encode( self.integer, self.size, self.format )


    def from_bytes(self, encoded, *args, **kwargs):
        length, self.integer = self.decode( encoded, self.size, self.format )
        return length, self.integer

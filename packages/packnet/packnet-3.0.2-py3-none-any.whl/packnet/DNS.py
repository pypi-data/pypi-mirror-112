"""

 PACKNET  -  c0mplh4cks

 DNS

     #===#==============#
     # 5 # Application  #
     #===#==============#
     | 4 | Transport    |
     |---|--------------|
     | 3 | Network      |
     |---|--------------|
     | 2 | Data Link    |
     |---|--------------|
     | 1 | Physical     |
     '---'--------------'


"""





# === Importing Dependencies === #
from random import randint
from . import Frame
from . import INT, NAME, IP







# === DNS Header === #
class Header(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.id = INT( randint(0, 0xffff), size=2 )
        self.flags = INT( 0x100, size=2 )
        self.questions = INT( 0, size=2 )
        self.answers = INT( 0, size=2 )
        self.authorities = INT( 0, size=2 )
        self.additionals = INT( 0, size=2 )
        self.protocol = None

        self.question = []
        self.answer = []
        self.authority = []
        self.additional = []

        self.structure = [
            "id",           # Identifier
            "flags",        # Flags
            "questions",    # Questions
            "answers",      # Answer records
            "authorities",  # Authority records
            "additionals"   # Additional records
        ]



    def rlen(self):
        super().rlen()
        for section in (self.question, self.answer, self.authority, self.additional):
            self.len.header.integer += sum([ len(part) for part in section ])


    def to_bytes(self, *args, **kwargs):
        self.questions.integer = len(self.question)
        self.answers.integer = len(self.answer)
        self.authorities.integer = len(self.authority)
        self.additionals.integer = len(self.additional)

        packet = super().to_bytes(*args, **kwargs)

        for section in (self.question, self.answer, self.authority, self.additional):
            for part in section:
                packet += part.to_bytes( header=packet )

        return packet


    def from_bytes(self, packet=b"", *args, **kwargs):
        i = super().from_bytes(packet, *args, **kwargs)[0]

        self.question = [ Query() for _ in range( self.questions.integer ) ]
        self.answer = [ Answer() for _ in range( self.answers.integer ) ]
        self.authority = [ Authority() for _ in range( self.authorities.integer ) ]
        self.additional = [ Additional() for _ in range( self.additionals.integer ) ]

        for section in (self.question, self.answer, self.authority, self.additional):
            for part in section:
                i += part.from_bytes( packet[i:], header=packet )[0]

        self.payload = packet[i:]
        self.rlen()

        return (i,)







# === Query === #
class Query(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = NAME()
        self.type = INT( 1, size=2 )
        self.classif = INT( 1, size=2 )

        self.structure = [
            "name",
            "type",
            "classif"
        ]







# === Answer === #
class Answer(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = NAME()
        self.type = INT( 1, size=2 )
        self.classif = INT( 1, size=2 )
        self.ttl = INT( 64, size=4 )
        self.cname = IP()

        self.structure = [
            "name",
            "type",
            "classif",
            "ttl",
            "len.payload"#,
            #"cname"
        ]



    def to_bytes(self, *args, **kwargs):
        self.payload = self.cname.to_bytes()

        return super().to_bytes(*args, **kwargs)


    def from_bytes(self, packet=b"", header=b"", *args, **kwargs):
        i = super().from_bytes(packet, header, *args, **kwargs)[0]

        if self.type.integer == 1:
            self.cname = IP( version=4 )
        elif self.type.integer == 28:
            self.cname = IP( version=6 )
        else:
            self.cname = NAME()

        i += self.cname.from_bytes( packet[i:], header )[0]
        self.payload = packet[i:]
        self.rlen()

        return (i,)







# === Authority === #
class Authority(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)







# === Additional === #
class Additional(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

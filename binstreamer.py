from struct import pack, unpack_from
from functools import partial
from ctypes import *

LE = 1
BE = 2

class BinaryStream():
    def __init__(self, stream, byteOrder=None):
        self.stream = stream
        self.byteOrder = byteOrder

    def __getattr__(self, name):
        if name[:4] == "read":
            return partial(self.read, name[4:].lower())
        if name[:5] == "write":
            return lambda data, byteOrder=None: self.write(data, name[5:].lower(), byteOrder)

    def _parsefmt(self, t):
        if t in ["float", float, c_float]:
            return ("f", 4)
        elif t in ["double", c_double]:
            return ("d", 8)
        elif t in ["i8", "int8", "byte", c_byte]:
            return ("b", 1)
        elif t in ["i16", "int16", "short", c_short]:
            return ("h", 2)
        elif t in ["i32", "int32", "int", int, c_int]:
            return ("i", 4)
        elif t in ["i64", "int64", "long", c_long, c_int64, c_longlong]:
            return ("q", 8)
        elif t in ["u8", "uint8", "ubyte", c_ubyte]:
            return ("B", 1)
        elif t in ["u16", "uint16", "ushort", c_ushort, c_uint16]:
            return ("H", 2)
        elif t in ["u32", "uint32", c_uint, c_uint32]:
            return ("I", 4)
        elif t in ["u64", "uint64", "ulong", c_ulong, c_uint64, c_ulonglong]:
            return ("Q", 8)
        elif t in ["char", c_char]:
            return ("c", 1)
        elif t in ["s", "str", "string"]:
            return ("s2", None)
        return (t, None)

    def read(self, length=-1, byteOrder=None):
        if type(length) != int:
            fmt = self._parsefmt(length)
            return self._unpack(fmt[0], fmt[1], byteOrder)
        return self.stream.read(length)

    def write(self, data, type_=None, byteOrder=None):
        if type_ is not None:
            fmt = self._parsefmt(type_)[0]
            self._pack(fmt, data, byteOrder)
        else:
            self.stream.write(data)

    def tell(self):
        return self.stream.tell()

    def seek(self, pos):
        return self.stream.seek(pos)

    @property
    def len(self):
        return self.stream.len

    @property
    def pos(self):
        return self.stream.pos

    def _unpack(self, fmt, length, byteOrder=None):
        byteOrder = byteOrder or self.byteOrder
        order_fmt = ""
        if byteOrder in ["LE", "<", LE]:
            order_fmt = "<"
        elif byteOrder in ["BE", ">", BE]:
            order_fmt = ">"
        if fmt[0] == "s" and length is None:
            length = self.read("uint" + str(8 * int(fmt[1:])), byteOrder)
            fmt = str(length) + fmt
        return unpack_from(order_fmt + fmt, self.stream.read(length))[0]

    def _pack(self, fmt, data, byteOrder=None):
        byteOrder = byteOrder or self.byteOrder
        order_fmt = ""
        if byteOrder in ["LE", "<", LE]:
            order_fmt = "<"
        elif byteOrder in ["BE", ">", BE]:
            order_fmt = ">"
        if fmt[0] == "s":
            self.write(len(data), "uint" + str(8 * int(fmt[1:])), byteOrder)
            self.stream.write(data)
        else:
            self.stream.write(pack(order_fmt + fmt, data))


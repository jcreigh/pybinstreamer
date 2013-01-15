pybinstreamer
=========

pybinstreamer is a simple and easy to use serializer. 'nuff said.

## Example
```python
from binstreamer import BinaryStream
from StringIO import StringIO
buf = StringIO("abcd")
stream = BinaryStream(buf)
print stream.read(4)
# abcd
stream.write("String, stored length", "s2")
stream.write(17000, "u16", "BE")  # Store 17000 as an unsigned 16-bit integer in Big Endian
stream.write(255, "u8")
stream.seek(0)
print stream.read(4)
# abcd
print stream.read("s2")
# String, stored length
print stream.read("u16", "LE")
# 26690 (since we read in Little Endian and stored in Big Endian)
print stream.read("i8")
# -1 (since we stored u8 and read i8)
```

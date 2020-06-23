import struct
import typing
import os

from .exceptions import OMFInvalidDataException


class BinaryParser:
    __slots__ = (
        "handle",
        "xor_key",
    )

    def __init__(self, handle: typing.BinaryIO) -> None:
        self.handle = handle
        self.xor_key: int = None

    def get_file_size(self) -> int:
        pos = self.get_pos()
        self.handle.seek(0, os.SEEK_END)
        size = self.handle.tell()
        self.set_pos(pos)
        return size

    def xor_data(self, data: bytes) -> bytearray:
        c = bytearray(data)
        for m in range(len(c)):
            c[m] = self.xor_key ^ c[m]

            self.xor_key += 1
            if self.xor_key > 255:
                self.xor_key = 0
        return c

    def write(self, data: bytes) -> None:
        if self.xor_key is not None:
            self.handle.write(self.xor_data(data))
        else:
            self.handle.write(data)

    def read(self, size: int) -> bytes:
        data = self.handle.read(size)
        if self.xor_key is not None:
            return bytes(self.xor_data(data))
        else:
            return data

    def set_xor_key(self, key: typing.Optional[int] = None):
        assert key is None or 0 <= key <= 255
        self.xor_key = key

    def skip(self, size: int) -> None:
        self.read(size)

    def get_pos(self) -> int:
        return self.handle.tell()

    def set_pos(self, pos: int) -> None:
        self.handle.seek(pos, os.SEEK_SET)

    def check_uint8(self, compare_to: int) -> None:
        got = self.get_uint8()
        if got != compare_to:
            raise OMFInvalidDataException(f"Got {got}, was expecting {compare_to}")

    def check_uint16(self, compare_to: int) -> None:
        got = self.get_uint16()
        if got != compare_to:
            raise OMFInvalidDataException(f"Got {got}, was expecting {compare_to}")

    def check_uint32(self, compare_to: int) -> None:
        got = self.get_uint32()
        if got != compare_to:
            raise OMFInvalidDataException(f"Got {got}, was expecting {compare_to}")

    def get_null_padded_str(self, max_length: int) -> str:
        chars = bytearray()
        ended = False
        for k in range(max_length):
            c = self.read(1)
            if c[0] == 0:
                ended = True
            if ended:
                continue
            chars.append(c[0])
        return chars.decode("cp437")

    def get_str(self, length: int) -> str:
        return self.read(length).decode("cp437") if length > 0 else ""

    def get_bytes(self, length: int) -> bytes:
        return self.read(length)

    def get_int8(self) -> int:
        return struct.unpack("<b", self.read(1))[0]

    def get_uint8(self) -> int:
        return struct.unpack("<B", self.read(1))[0]

    def get_int16(self) -> int:
        return struct.unpack("<h", self.read(2))[0]

    def get_uint16(self) -> int:
        return struct.unpack("<H", self.read(2))[0]

    def get_int32(self) -> int:
        return struct.unpack("<i", self.read(4))[0]

    def get_uint32(self) -> int:
        return struct.unpack("<I", self.read(4))[0]

    def get_float(self) -> float:
        return struct.unpack("<f", self.read(4))[0]

    def get_boolean(self) -> bool:
        return self.get_uint8() == 1

    def get_var_str(self, size_includes_zero: bool = False) -> str:
        m_len = self.get_uint16()
        if m_len == 0 and size_includes_zero:
            return ""
        data = self.get_str(m_len - (1 if size_includes_zero else 0))
        self.check_uint8(0)
        return data

    def put_null_padded_str(self, data: str, max_length: int) -> None:
        buf = data.encode("cp437")[:max_length]
        left = max_length - len(buf)
        self.write(buf)
        for _ in range(left):
            self.write(b"\0")

    def put_str(self, data: str) -> None:
        self.write(data.encode("cp437"))

    def put_bytes(self, data: bytes) -> None:
        self.write(data)

    def put_int8(self, data: int) -> None:
        self.write(struct.pack("<b", data))

    def put_uint8(self, data: int) -> None:
        self.write(struct.pack("<B", data))

    def put_int16(self, data: int) -> None:
        self.write(struct.pack("<h", data))

    def put_uint16(self, data: int) -> None:
        self.write(struct.pack("<H", data))

    def put_int32(self, data: int) -> None:
        self.write(struct.pack("<i", data))

    def put_uint32(self, data: int) -> None:
        self.write(struct.pack("<I", data))

    def put_float(self, data: float) -> None:
        self.write(struct.pack("<f", data))

    def put_boolean(self, data: bool) -> None:
        self.put_uint8(1 if data else 0)

    def put_var_str(self, data: str, size_includes_zero: bool = False) -> None:
        m_data = data.encode()
        m_len = len(m_data)
        if m_len == 0 and size_includes_zero:
            self.put_uint16(0)
            return
        self.put_uint16(m_len + (1 if size_includes_zero else 0))
        self.write(m_data)
        self.put_uint8(0)

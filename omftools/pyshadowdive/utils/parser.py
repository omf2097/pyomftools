import struct
import typing

from .exceptions import OMFInvalidDataException


class BinaryParser:
    __slots__ = ('handle',)

    def __init__(self, handle: typing.BinaryIO) -> None:
        self.handle = handle

    def get_pos(self) -> int:
        return self.handle.tell()

    def check_uint8(self, compare_to: int) -> None:
        got = self.get_uint8()
        if got != compare_to:
            raise OMFInvalidDataException(
                f"Got {got}, was expecting {compare_to}")

    def check_uint16(self, compare_to: int) -> None:
        got = self.get_uint16()
        if got != compare_to:
            raise OMFInvalidDataException(
                f"Got {got}, was expecting {compare_to}")

    def check_uint32(self, compare_to: int) -> None:
        got = self.get_uint32()
        if got != compare_to:
            raise OMFInvalidDataException(
                f"Got {got}, was expecting {compare_to}")

    def get_str(self, length: int) -> str:
        return self.handle.read(length).decode() if length > 0 else ''

    def get_bytes(self, length: int) -> bytes:
        return self.handle.read(length)

    def get_int8(self) -> int:
        return struct.unpack('<b', self.handle.read(1))[0]

    def get_uint8(self) -> int:
        return struct.unpack('<B', self.handle.read(1))[0]

    def get_int16(self) -> int:
        return struct.unpack('<h', self.handle.read(2))[0]

    def get_uint16(self) -> int:
        return struct.unpack('<H', self.handle.read(2))[0]

    def get_int32(self) -> int:
        return struct.unpack('<i', self.handle.read(4))[0]

    def get_uint32(self) -> int:
        return struct.unpack('<I', self.handle.read(4))[0]

    def get_float(self) -> float:
        return struct.unpack('<f', self.handle.read(4))[0]

    def get_boolean(self) -> bool:
        return self.get_uint8() == 1

    def get_var_str(self, size_includes_zero: bool = False) -> str:
        m_len = self.get_uint16()
        if m_len == 0 and size_includes_zero:
            return ''
        data = self.get_str(m_len - (1 if size_includes_zero else 0))
        self.check_uint8(0)
        return data

    def put_str(self, data: str) -> None:
        self.handle.write(data.encode())

    def put_bytes(self, data: bytes) -> None:
        self.handle.write(data)

    def put_int8(self, data: int) -> None:
        self.handle.write(struct.pack('<b', data))

    def put_uint8(self, data: int) -> None:
        self.handle.write(struct.pack('<B', data))

    def put_int16(self, data: int) -> None:
        self.handle.write(struct.pack('<h', data))

    def put_uint16(self, data: int) -> None:
        self.handle.write(struct.pack('<H', data))

    def put_int32(self, data: int) -> None:
        self.handle.write(struct.pack('<i', data))

    def put_uint32(self, data: int) -> None:
        self.handle.write(struct.pack('<I', data))

    def put_float(self, data: float) -> None:
        self.handle.write(struct.pack('<f', data))

    def put_boolean(self, data: bool) -> None:
        self.put_uint8(1 if data else 0)

    def put_var_str(self, data: str, size_includes_zero: bool = False) -> None:
        m_data = data.encode()
        m_len = len(m_data)
        if m_len == 0 and size_includes_zero:
            self.put_uint16(0)
            return
        self.put_uint16(m_len + (1 if size_includes_zero else 0))
        self.handle.write(m_data)
        self.put_uint8(0)

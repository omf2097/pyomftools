import struct
import json


class OMFException(Exception):
    pass


class OMFInvalidDataException(OMFException):
    pass


class OMFParser(object):
    def __init__(self, handle):
        self.handle = handle

    def get_pos(self):
        return self.handle.tell()

    def check_uint8(self, compare_to):
        got = self.get_uint8()
        if got != compare_to:
            raise OMFInvalidDataException("Got {}, was expecting {}".format(got, compare_to))

    def check_uint16(self, compare_to):
        got = self.get_uint16()
        if got != compare_to:
            raise OMFInvalidDataException("Got {}, was expecting {}".format(got, compare_to))

    def check_uint32(self, compare_to):
        got = self.get_uint32()
        if got != compare_to:
            raise OMFInvalidDataException("Got {}, was expecting {}".format(got, compare_to))

    def get_str(self, length):
        return self.handle.read(length).decode() if length > 0 else ''

    def get_bytes(self, length):
        return self.handle.read(length)

    def get_int8(self):
        return struct.unpack('<b', self.handle.read(1))[0]

    def get_uint8(self):
        return struct.unpack('<B', self.handle.read(1))[0]

    def get_int16(self):
        return struct.unpack('<h', self.handle.read(2))[0]

    def get_uint16(self):
        return struct.unpack('<H', self.handle.read(2))[0]

    def get_int32(self):
        return struct.unpack('<i', self.handle.read(4))[0]

    def get_uint32(self):
        return struct.unpack('<I', self.handle.read(4))[0]

    def get_float(self):
        return struct.unpack('<f', self.handle.read(4))[0]

    def get_boolean(self):
        return self.get_uint8() == 1

    def get_var_str(self, size_includes_zero=False):
        m_len = self.get_uint16()
        if m_len == 0 and size_includes_zero:
            return ''
        data = self.get_str(m_len - (1 if size_includes_zero else 0))
        self.check_uint8(0)
        return data

    def put_str(self, data):
        self.handle.write(data.encode())

    def put_bytes(self, data):
        self.handle.write(data)

    def put_int8(self, data):
        self.handle.write(struct.pack('<b', data))

    def put_uint8(self, data):
        self.handle.write(struct.pack('<B', data))

    def put_int16(self, data):
        self.handle.write(struct.pack('<h', data))

    def put_uint16(self, data):
        self.handle.write(struct.pack('<H', data))

    def put_int32(self, data):
        self.handle.write(struct.pack('<i', data))

    def put_uint32(self, data):
        self.handle.write(struct.pack('<I', data))

    def put_float(self, data):
        self.handle.write(struct.pack('<f', data))

    def put_boolean(self, data):
        self.put_uint8(1 if data else 0)

    def put_var_str(self, data, size_includes_zero=False):
        m_data = data.encode()
        m_len = len(m_data)
        if m_len == 0 and size_includes_zero:
            self.put_uint16(0)
            return
        self.put_uint16(m_len + (1 if size_includes_zero else 0))
        self.handle.write(m_data)
        self.put_uint8(0)


class OMFObjectMixin(object):
    def read(self, parser):
        pass

    def write(self, parser):
        pass

    def serialize(self):
        return {}

    def unserialize(self, data):
        pass


class OMFEntrypointMixin(OMFObjectMixin):
    def load_native(self, filename):
        with open(filename, 'rb') as handle:
            self.read(OMFParser(handle))

    def save_native(self, filename):
        with open(filename, 'wb') as handle:
            self.write(OMFParser(handle))

    def load_json(self, filename):
        with open(filename, 'rb') as handle:
            self.from_json(handle.read().decode())

    def save_json(self, filename, **kwargs):
        with open(filename, 'wb') as handle:
            handle.write(self.to_json(**kwargs).encode())

    def to_json(self, **kwargs):
        return json.dumps(self.serialize(), **kwargs)

    def from_json(self, data):
        return self.unserialize(json.loads(data))

import wave
import typing


def save_wav(data: typing.List[int], filename: str):
    with wave.open(filename, 'wb') as fd:
        fd.setnchannels(1)
        fd.setsampwidth(1)
        fd.setframerate(8000)
        fd.writeframes(bytes(data))

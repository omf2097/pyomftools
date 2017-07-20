from omftools.pyshadowdive.af import AFFile

_current_file = AFFile()
_current_file_name = None


def load_file(filename):
    global _current_file
    global _current_file_name
    f = AFFile()
    try:
        f.load_native(filename)
    except:
        raise
    else:
        _current_file = f
        _current_file_name = filename


def save_to(filename):
    global _current_file
    global _current_file_name
    _current_file.save_native(filename)
    _current_file_name = filename


def new_file():
    global _current_file
    global _current_file_name
    _current_file_name = None
    _current_file = AFFile()


def get_current_file():
    global _current_file
    return _current_file


def get_current_file_name():
    global _current_file_name
    return _current_file_name

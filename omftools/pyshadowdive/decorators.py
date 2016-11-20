from cerberus import Validator

from .protos import OMFInvalidDataException


def validate_schema(schema):
    def _inner_has_privileges(method):
        def inner(instance, *args, **kwargs):
            v = Validator(schema)
            if v.validate(args[0]):
                method(instance, *args, **kwargs)
            else:
                err_field, err_messages = v.errors.popitem()
                err_message = err_messages[0]
                raise OMFInvalidDataException("{}: {}".format(err_field, err_message))
        return inner
    return _inner_has_privileges
